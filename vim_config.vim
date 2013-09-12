let g:wikilang='uk'
let g:wikidomain='.wikipedia.org'

function! ChangeEndpoint()
    call system("./cli.py endpoint " . g:wikilang . g:wikidomain)
endfunction
call ChangeEndpoint()

function! ChangeLang(code)
    let g:wikilang = a:code
    echo 'Current wiki language: ' . a:code
    call ChangeEndpoint()
endfunction
command -complete=customlist,LanguagesCompletion -nargs=1 Wikil call ChangeLang(<f-args>)

function! LanguagesCompletion(ArgLead, CmdLine, CursorPos)
    return ['uk', 'en']
endfunction

function! LaguageToggle()
    if g:wikilang == 'uk'
        call ChangeLang('en')
    else
        call ChangeLang('uk')
    endif
endfunction

map <down> :call LaguageToggle()<CR>

command! -complete=custom,WikiPageNameCompletion -nargs=1 Wikie call WikiE(<f-args>)
function! WikiPageNameCompletion(ArgLead, CmdLine, CursorPos)
    return system("./cli.py autocomplete " . a:ArgLead)
endfunction
function! WikiE(pagename)
    enew
    execute ":r!./cli.py read " . escape(a:pagename, '()')
    set syntax=wiki
    let w:pagename = a:pagename
    normal ggdd
endfunction

" open wikilink in new tab
nmap w] "wyi[<F7>:Wikie <C-R>w

command! -nargs=? Wikiw call WikiW(<f-args>)
function! WikiW(...)
    let pagename = (a:0 >= 1) && a:1 ? a:1 : w:pagename
    execute ":w !./cli.py write " . pagename
endfunction
