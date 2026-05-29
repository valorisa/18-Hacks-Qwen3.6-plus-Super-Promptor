#NoEnv
#SingleInstance Force
#Persistent

; ═══════════════════════════════════════════════════════════════
; PSMUX GLOBAL HOTKEYS - Windows 11 (Sans conflit)
; Fonctionne même quand psmux n'est pas en focus
; ═══════════════════════════════════════════════════════════════

; ─────────────────────────────────────────────────────────────
; TOUCHES AVEC LA touche WINDOWS (Win)
; ─────────────────────────────────────────────────────────────

; Win+M : Lancer psmux
#m::
    Run, psmux
return

; Win+Shift+M : Quick mux clipboard
#+m::
    originalClip := Clipboard
    Send, ^c
    Sleep, 150
    clipContent := Clipboard
    Clipboard := originalClip
    
    if (clipContent != "") {
        Run, psmux mux -i "%clipContent%"
    }
return

; Win+P : Toggle panel visibility
#p::
    Run, psmux toggle-panels
return

; Win+S : Quick save config
#s::
    Run, psmux config --save
return

; Win+Q : Emergency stop
#q::
    Run, psmux kill
return

; Win+R : Reload shortcuts
#r::
    Run, psmux shortcuts --reload
return

; Win+H : Show/hide psmux (toggle)
#h::
    IfWinExist, psmux
    {
        IfWinActive, psmux
            WinMinimize
        else
            WinActivate
    }
    else
        Run, psmux
return

; Win+T : Quick preset streaming
#t::
    Run, psmux mux --preset streaming
return

; ─────────────────────────────────────────────────────────────
; COMBINAISONS AVEC CTRL+ALT
; ─────────────────────────────────────────────────────────────

; Ctrl+Alt+M : Mux rapide dossier courant
^!m::
    Run, psmux mux --batch .
return

; Ctrl+Alt+P : Ouvrir panel préférences
^!p::
    Run, psmux preferences
return

; Ctrl+Alt+E : Export config actuelle
^!e::
    Run, psmux config --export "%USERPROFILE%\.psmux\snapshot.yaml"
return

; Ctrl+Alt+R : Relancer psmux
^!r::
    Run, psmux kill
    Sleep, 500
    Run, psmux
return

; Ctrl+Alt+O : Open file dialog
^!o::
    Run, psmux file --open
return

; Ctrl+Alt+L : Show log panel
^!l::
    Run, psmux log --show
return

; ─────────────────────────────────────────────────────────────
; CTRL+ALT + CHIFFRES (Presets)
; ─────────────────────────────────────────────────────────────

; Ctrl+Alt+1 : Preset mobile
^!1::
    Run, psmux mux --preset mobile
return

; Ctrl+Alt+2 : Preset streaming
^!2::
    Run, psmux mux --preset streaming
return

; Ctrl+Alt+3 : Preset archival
^!3::
    Run, psmux mux --preset archival
return

; Ctrl+Alt+4 : Preset broadcast
^!4::
    Run, psmux mux --preset broadcast
return

; Ctrl+Alt+5 : Preset web
^!5::
    Run, psmux mux --preset web
return

; ─────────────────────────────────────────────────────────────
; NOTIFICATIONS SYSTÈME
; ─────────────────────────────────────────────────────────────

#IfWinActive, psmux
    ; Raccourcis uniquement quand psmux est actif
    F9::
        Run, psmux export --last
    return
    
    F10::
        Run, psmux history
    return
#IfWinActive

; ─────────────────────────────────────────────────────────────
; CONFIGURATION
; ─────────────────────────────────────────────────────────────

; Pour personnaliser, éditez ce fichier
; Documentation AutoHotkey : https://www.autohotkey.com/docs/

; Pour lancer au démarrage Windows :
; 1. Copier ce fichier dans %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
; 2. Ou utiliser Windows Task Scheduler
