===========
B Wiki Bot
===========
There was a wiki bot, so I decided to create also b wiki bot.

It should work on Python 3 and Python 2 both. :snake: Or just on Python 3, but I'll try to support both.

After installation run command bwikibot, and you should see something like this:

    now           - Prints current ISO-formatted zulu time
    bulk_delete   - Delete all pages of primary wiki which starts with prefix
    autocomplete  - Print list of page names which starts from passed prefix
    spell         - Make autocorrection with dictionary
    bulk_delete2  - Delete all pages of secondary wiki which starts with prefix
    translate     - Automate translation of wikitext from one language to another
                      -f from_lang (for example 'en')
                      -t to lang (for example 'uk')
    login2        - Login to secondary wiki
    write         - Read text from stdio and save to page with name passed in param
    read          - Print page which's name passed in param to stdout
    logout2       - Delete session file
    login         - Login to primary wiki
    throttle      - Set or get delay between queries.
    serve         - web.serve has no docstring
    bulk_export   - Copy pages with given prefix from primary wiki to secondary.
    read2         - Print page from secondary wiki which's name passed in param to stdout
    check_uploads - Check and mark new files for licensing issues,
                      and send messages to uploaders.
    throttle2     - Set or get delay between queries for secondary wiki.
    write2        - Read text from stdio and save to page on secondary wiki with name passed in param
    autocomplete2 - Print list of page names which starts from passed prefix for secondary wiki
    import_poster - Імпортувати постер для статті, і додати його в шаблон фільму.
                      Перший параметр - назва статті фільму.
                      другий - джерело. url або мовний код. Якщо мовний код - автора та
    logout        - Delete session file

That is list of subcommands which is supported by current version of robot.
