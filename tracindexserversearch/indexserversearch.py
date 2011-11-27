# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 Patrick Martin <patrickmmartin@gmail.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at http://trac.edgewall.com/license.html.

from trac.core import *
from trac.Search import ISearchSource, shorten_result
from trac.util import Markup, escape
from trac.mimeview.api import Mimeview
import win32com.client
from pythoncom import CoInitialize, CoUninitialize, com_error
com= win32com.client.Dispatch
con= win32com.client.constants

__all__ = ['IndexServerProxy']

class IndexServerProxy(Component):
  """Component to pass on queries to the Index Server components."""   
  implements(ISearchSource)

  def get_index_server_results(self, repo, wordlist):
    
      if not self.env.config.get('indexserver-search', 'catalogue-root', ''):
        raise TracError("Index Server plugin is not " \
                "configured correctly. Set the 'catalogue-root' option " \
                "under the 'indexserver-search' section to the full " \
                "(case-correct) path of the root of the catalogued source.")

      #this sets up a handler for unicode conversion
      # ? is this more efficient outside the loop?
      to_unicode = Mimeview(self.env).to_unicode        

      checkoutroot = self.env.config.get('indexserver-search', 'catalogue-root', '')
      CoInitialize()
      try:
        fso = com("Scripting.FileSystemObject")
        if not fso.FolderExists(checkoutroot):
          raise TracError("Index Server plugin is not " \
                  "configured correctly. The folder referred to in the 'catalogue-root' option '" 
                  + checkoutroot + 
                  "' under the 'indexserver-search' section does not exist.")
        
        query = com('IXSSO.Query')

        query.Dialect = 2
        query.Columns = "rank, filename, path, characterization"
        phrase   = ' '.join(wordlist)

        querystr = phrase
        querystr += " AND NOT {prop name=path}{regex}*\.svn*{/regex}"

        query.Query = querystr;

        query.SortBy = "rank[d]"  
        query.Catalog = "Source Catalogue"
        query.OptimizeFor      = "recall"
        query.MaxRecords       = 100

        self.env.log.debug("index server query is: " + querystr )
        try:
          result = query.CreateRecordset("sequential")

        except com_error, (hr, msg, exc, arg):
          if exc is None:
            print "There is no extended error information"
            raise TracError("Index Server raised exception on query [" + phrase + "] " \
                              " details: %d: %s" % (hr, msg) +
                              "note that the $ and # characters need to be escaped where not used as special identifiers. " \
                              "See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/indexsrv/html/ixarch_1n5f.asp " \
                              " for more details.")
          else:
            wcode, source, text, helpFile, helpId, scode = exc

            raise TracError("Index Server raised exception on query [" + phrase + "] " \
                              " details: " \
                              "the source of the error is '" + source + "' " +
                              "the error message is '" + text + "' " +
##                              "more info can be found in %s (id=%d) " % (helpFile, helpId) +
                              "note that the $ and # characters need to be escaped where not used as special identifiers. " \
                              "See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/indexsrv/html/ixarch_1n5f.asp " \
                              " for more details.")
            
 	
                    
        query = None

        hits = list()


        while not (result.EOF):
            # note: path in search results is lower cased
            indexpath = to_unicode(result.Fields('path'), "utf_16")
            # index might not be up completely up to date, and has old files
            if fso.FileExists(indexpath):
              # need to get correctly cased file name, and convert into respository URL
              # this filename should have the desired case
              fo = fso.GetFile(indexpath)
              path = to_unicode(fo.Path, "utf_16")
              filename = to_unicode(fo.Name, "utf_16")
              fo = None
              # strip checkout root folder
              url = path.replace(checkoutroot, "")
              # and URL-ise
              url = url.replace("\\", '/')

              # attempt to get the repository node relating to the url
              # this may fail if the source index is out of date,
              # which means the hit may not be present at that url,
              # so skip these exceptions
              node = None
              try:
                node = repo.get_node(url)
                change = repo.get_changeset(node.rev)
              except TracError, e:
                self.env.log.warning('ignoring failure to obtain node at ' + url + ': ' + e)

              # got up to date node - get the details
              if node:    
                # attempt to use index server "characterization" field
                # for files set as application/octet-stream, if present
                # as index server indexes Office documents,
                # should pick up abstract of those binary files OK
                content = None
                characterization = result.Fields('characterization')
                if ((node.get_content_type() == "application/octet-stream") and (characterization <> None)):
                  try:
                    content = to_unicode(characterization, "utf_16")
                    self.env.log.debug('got characterization field for node ' + url)
                  except UnicodeEncodeError, e:
                    content = None
                    self.env.log.warning(e)
                    self.env.log.warning('ignoring failure for conversion of characterization field for node ' + url)
                                      
                # if not binary or no abstract, or there was a UnicodeEncodeError ?!
                # pull back the node content
                if not content:    
                  contentstream = node.get_content()
                  if contentstream:
                    content = to_unicode(contentstream.read(), node.get_content_type())
                    self.env.log.debug('got content from repository for node ' + url)
                  else:
                    self.env.log.debug('no content from repository for node ' + url)                  
                            
                hit = list()
                  
                hit.append(self.env.href.browser(url))
                hit.append(filename + ": " + url)
                hit.append(change.date)
                hit.append(change.author)
                hit.append(shorten_result(content, wordlist))
                hits.append(hit)
                 
                result.MoveNext()
                
        
        result = None
        fso = None
        return hits

      # todo proper clean -up even when the plug-in is in big trouble
      finally:
        CoUninitialize()


  # ISearchSource methods

##         The events returned by this function must be tuples of the form 
##         (internalname, friendlyname, onbydefault). 
  
  def get_search_filters(self, req):
      # this Component will support an "Index Server" search
      # todo: have a content, property, advanced search?
      yield ('indexserver', 'Index Server', 1)

##         The events returned by this function must be tuples of the form 
##         (href, title, date, author, excerpt). 

  def get_search_results(self, req, query, filters):
    if 'indexserver' not in filters:
      return
    repo = self.env.get_repository(req.authname)
    if not isinstance(query, list):
      query = query.split()
    query = [q.lower() for q in query]
    
    for result in self.get_index_server_results(repo, query):
      yield result

