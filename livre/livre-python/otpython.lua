-- =====================================================================
--  otpython.lua — moteur des blocs de code du livre Python OptiTAB
--  * capture verbatim des environnements code / sortie / console / erreur
--    (les lignes sont lues telles quelles dans le fichier source) ;
--  * coloration syntaxique de Python (aucune dépendance externe) ;
--  * rendu ligne par ligne : chaque ligne est une \hbox, la boîte peut
--    se couper entre deux lignes, jamais après la 1re ni avant la dernière.
--  Conventions dans les sources :
--    «texte»   dans une sortie ou une console : texte tapé par l'utilisateur
--    # <3>     en fin de ligne de code : pastille de renvoi n° 3
--    ___       (3 tirets bas ou plus) : trou à compléter
-- =====================================================================
otpy = otpy or {}

---------------------------------------------------------------------------
-- Capture des lignes d'un environnement
---------------------------------------------------------------------------
local lignes, env_courant = {}, nil

local function rappel(buf)
  local b = buf:gsub("\r$", "")
  if b:match("^%s*\\end{" .. env_courant .. "}") then
    luatexbase.remove_from_callback("process_input_buffer", "otpy.capture")
    return b
  end
  lignes[#lignes + 1] = b
  return "%"
end

function otpy.capture(env)
  lignes, env_courant = {}, env
  luatexbase.add_to_callback("process_input_buffer", rappel, "otpy.capture")
end

local function nettoyer(t)
  while #t > 0 and t[1]:match("^%s*$") do table.remove(t, 1) end
  while #t > 0 and t[#t]:match("^%s*$") do table.remove(t) end
  for k, l in ipairs(t) do t[k] = l:gsub("%s+$", "") end
  return t
end

---------------------------------------------------------------------------
-- Écriture dans TeX : texte « autre » (catcodes 12), espaces de largeur fixe,
-- trous ___ dessinés
---------------------------------------------------------------------------
local function brut(s)
  -- espaces : \otSp{n} (crénage de n caractères), le reste en catcode 12
  local pos = 1
  while pos <= #s do
    local a, b = s:find(" +", pos)
    if not a then tex.sprint(-2, s:sub(pos)) break end
    if a > pos then tex.sprint(-2, s:sub(pos, a - 1)) end
    tex.sprint("\\otSp{" .. (b - a + 1) .. "}")
    pos = b + 1
  end
end

local function texte(s)
  if not s or s == "" then return end
  local pos = 1
  while pos <= #s do
    local a, b = s:find("___+", pos)
    if not a then brut(s:sub(pos)) break end
    if a > pos then brut(s:sub(pos, a - 1)) end
    tex.sprint("\\otTrouCode{" .. (b - a + 1) .. "}")
    pos = b + 1
  end
end

local function style(st, s)
  if not s or s == "" then return end
  tex.sprint("{\\otSty" .. st .. " ")
  texte(s)
  tex.sprint("}")
end

---------------------------------------------------------------------------
-- Coloration de Python
---------------------------------------------------------------------------
local function ensemble(liste)
  local t = {}
  for m in liste:gmatch("%S+") do t[m] = true end
  return t
end
local MOTSCLES = ensemble([[and as assert async await break class continue def del elif else
  except finally for from global if import in is lambda nonlocal not or pass raise return try
  while with yield]])
local CONSTANTES = ensemble("True False None")
local NATIVES = ensemble([[abs all any ascii bin bool breakpoint bytearray bytes callable chr
  classmethod compile complex delattr dict dir divmod enumerate eval exec filter float format
  frozenset getattr globals hasattr hash help hex id input int isinstance issubclass iter len
  list locals map max memoryview min next object oct open ord pow print property range repr
  reversed round set setattr slice sorted staticmethod str sum super tuple type vars zip]])
local function est_exception(m)
  return m:match("Error$") or m:match("Exception$") or m:match("Warning$")
      or m == "KeyboardInterrupt" or m == "StopIteration" or m == "SystemExit"
end

local etat = nil  -- chaîne triple en cours sur plusieurs lignes : { delim, f }

-- chaîne f : les {expressions} sont mises en évidence
local function rendu_fchaine(s)
  local i, n, debut = 1, #s, 1
  while i <= n do
    local c = s:sub(i, i)
    if (c == "{" or c == "}") and s:sub(i + 1, i + 1) == c then
      i = i + 2
    elseif c == "{" then
      style("Str", s:sub(debut, i - 1))
      local prof, j = 1, i + 1
      while j <= n and prof > 0 do
        local d = s:sub(j, j)
        if d == "{" then prof = prof + 1 elseif d == "}" then prof = prof - 1 end
        j = j + 1
      end
      style("Interp", s:sub(i, j - 1))
      i, debut = j, j
    else
      i = i + 1
    end
  end
  style("Str", s:sub(debut))
end

local function rendu_chaine(s, f)
  if f then rendu_fchaine(s) else style("Str", s) end
end

local function colorer(l)
  local i, n = 1, #l
  if etat then
    local a, b = l:find(etat.delim, 1, true)
    if not a then rendu_chaine(l, etat.f) return end
    rendu_chaine(l:sub(1, b), etat.f)
    etat = nil
    i = b + 1
  end
  local precedent = nil
  local debut_ligne = true
  while i <= n do
    local reste = l:sub(i)
    local esp = reste:match("^ +")
    if esp then
      texte(esp) i = i + #esp
    elseif reste:sub(1, 1) == "#" then
      local num = reste:match("^#%s*<(%d+)>%s*$")
      if num then
        tex.sprint("\\otRepere{" .. num .. "}")
      else
        style("Com", reste)
      end
      i = n + 1
    elseif reste:match("^___") then
      local m = reste:match("^_+")
      texte(m) i = i + #m
    elseif reste:match("^[rRbBfFuU]?[rRbBfFuU]?['\"]")
        and not l:sub(i - 1, i - 1):match("[%w_]") then
      local pre = reste:match("^([rRbBfFuU]?[rRbBfFuU]?)['\"]")
      local f = pre:lower():find("f", 1, true) ~= nil
      local q = reste:sub(#pre + 1, #pre + 1)
      local triple = reste:sub(#pre + 1, #pre + 3) == q:rep(3)
      local delim = triple and q:rep(3) or q
      local j = #pre + #delim + 1
      local fin = nil
      while j <= #reste do
        local c = reste:sub(j, j)
        if c == "\\" then j = j + 2
        elseif reste:sub(j, j + #delim - 1) == delim then fin = j + #delim - 1 break
        else j = j + 1 end
      end
      if pre ~= "" then style("Str", pre) end
      if fin then
        rendu_chaine(reste:sub(#pre + 1, fin), f)
        i = i + fin
      else
        rendu_chaine(reste:sub(#pre + 1), f)
        if triple then etat = { delim = delim, f = f } end
        i = n + 1
      end
    elseif reste:match("^%d") or reste:match("^%.%d") then
      local m = reste:match("^0[xXoObB][%x_]+")
        or reste:match("^%d[%d_]*%.?[%d_]*[eE][+-]?%d+j?")
        or reste:match("^%d[%d_]*%.?[%d_]*j?")
        or reste:match("^%.%d[%d_]*[eE][+-]?%d+j?")
        or reste:match("^%.%d[%d_]*j?")
      style("Num", m) i = i + #m
    elseif reste:match("^[%a_]") then
      local m = reste:match("^[%a_][%w_]*")
      local apres_point = l:sub(i - 1, i - 1) == "."
      if precedent == "def" then style("Fonc", m)
      elseif precedent == "class" then style("Classe", m)
      elseif MOTSCLES[m] then style("Kw", m)
      elseif CONSTANTES[m] then style("Const", m)
      elseif NATIVES[m] and not apres_point then style("Natif", m)
      elseif est_exception(m) and not apres_point then style("Exc", m)
      else texte(m) end
      precedent = (m == "def" or m == "class") and m or nil
      i = i + #m
    elseif debut_ligne and reste:match("^@[%a_][%w_%.]*") then
      local m = reste:match("^@[%a_][%w_%.]*")
      style("Deco", m) i = i + #m
    else
      local m = reste:match("^[%z\1-\127\194-\244][\128-\191]*")
      if m:match("^[%+%-%*/%%=<>!&|%^~]$") then style("Op", m) else texte(m) end
      i = i + #m
    end
    debut_ligne = false
  end
end

---------------------------------------------------------------------------
-- Sorties : «saisie» de l'utilisateur
---------------------------------------------------------------------------
local function segments_sortie(s)
  local pos = 1
  while true do
    local a, b = s:find("«", pos, true)
    if not a then texte(s:sub(pos)) break end
    local c, d = s:find("»", b + 1, true)
    if not c then texte(s:sub(pos)) break end
    texte(s:sub(pos, a - 1))
    tex.sprint("\\otSaisie{")
    texte(s:sub(b + 1, c - 1))
    tex.sprint("}")
    pos = d + 1
  end
end

local function numeros(spec)
  local t = {}
  for morceau in (spec or ""):gmatch("[^,%s]+") do
    local a, b = morceau:match("^(%d+)%-(%d+)$")
    if a then for k = tonumber(a), tonumber(b) do t[k] = true end
    elseif tonumber(morceau) then t[tonumber(morceau)] = true end
  end
  return t
end

-- 1 = pas de coupure après cette ligne (1re ligne, avant-dernière ligne)
local function attache(k, total)
  return (k == 1 or k == total - 1) and 1 or 0
end

local function est_erreur(l)
  return l:match("^[%w_%.]*Error:") or l:match("^[%w_%.]*Error$")
      or l:match("^[%w_%.]*Exception:") or l:match("^KeyboardInterrupt")
end

-- repère les blocs d'erreur : 1 = ligne du traceback, 2 = ligne finale
local function marquer_erreurs(t, console)
  local erreur = {}
  local i = 1
  while i <= #t do
    local l = t[i]
    if l:match("^Traceback %(most recent call last%):") or l:match("^  File \"") then
      local j = i
      while j <= #t and not est_erreur(t[j]) and not (console and t[j]:match("^>>>")) do
        j = j + 1
      end
      if j <= #t and est_erreur(t[j]) then
        for k = i, j do erreur[k] = (k == j) and 2 or 1 end
        i = j + 1
      else
        i = i + 1
      end
    elseif est_erreur(l) then
      erreur[i] = 2
      i = i + 1
    else
      i = i + 1
    end
  end
  return erreur
end

---------------------------------------------------------------------------
-- Rendus
---------------------------------------------------------------------------
function otpy.rendu_code(marques, premier, debut, fin)
  local t = nettoyer(lignes)
  local m = numeros(marques)
  premier = tonumber(premier) or 1
  etat = nil
  tex.sprint((debut or "\\otBoiteCodeDebut") .. "{" .. #t .. "}")
  for k, l in ipairs(t) do
    tex.sprint("\\otLigneCodeDebut{" .. (premier + k - 1) .. "}{" .. (m[k] and 1 or 0) .. "}")
    colorer(l)
    tex.sprint("\\otLigneCodeFin{" .. attache(k, #t) .. "}")
  end
  tex.sprint(fin or "\\otBoiteCodeFin")
  etat = nil
end

function otpy.rendu_idleediteur()
  otpy.rendu_code("", "1", "\\otBoiteIdleEditeurDebut", "\\otBoiteIdleEditeurFin")
end

local function rendu_ecran(t, debut, fin, console)
  local erreur = marquer_erreurs(t, console)
  etat = nil
  tex.sprint(debut .. "{" .. #t .. "}")
  for k, l in ipairs(t) do
    tex.sprint("\\otLigneDebut ")
    -- pastille de renvoi en fin de ligne : « texte  <<2>> »
    local corps, renvoi = l:match("^(.-)%s*<<(%d+)>>$")
    if corps then l = corps end
    local p, code
    if console then
      p, code = l:match("^(>>>) ?(.*)$")
      if not p then p, code = l:match("^(%.%.%.) ?(.*)$") end
    end
    if p then
      tex.sprint("\\otPrompt{" .. p .. "}")
      colorer(code)
    elseif erreur[k] == 1 then
      tex.sprint("\\otErreurLigne{") segments_sortie(l) tex.sprint("}")
    elseif erreur[k] == 2 then
      tex.sprint("\\otErreurFin{") segments_sortie(l) tex.sprint("}")
    else
      tex.sprint("\\otResultat{") segments_sortie(l) tex.sprint("}")
    end
    if renvoi then tex.sprint("\\otSp{2}\\otRepere{" .. renvoi .. "}") end
    tex.sprint("\\otLigneFin{" .. attache(k, #t) .. "}")
  end
  tex.sprint(fin)
  etat = nil
end

function otpy.rendu_sortie()
  rendu_ecran(nettoyer(lignes), "\\otBoiteSortieDebut", "\\otBoiteSortieFin", false)
end
function otpy.rendu_erreur()
  rendu_ecran(nettoyer(lignes), "\\otBoiteErreurDebut", "\\otBoiteErreurFin", false)
end
function otpy.rendu_console()
  rendu_ecran(nettoyer(lignes), "\\otBoiteConsoleDebut", "\\otBoiteConsoleFin", true)
end
function otpy.rendu_idleshell()
  rendu_ecran(nettoyer(lignes), "\\otBoiteIdleShellDebut", "\\otBoiteIdleShellFin", true)
end

-- Code coloré en ligne (illustrations) : \otCodeIllus{texte}
-- (dans l'argument TeX, % et # s'écrivent \% et \#)
function otpy.colorer_texte(s)
  s = s:gsub("\\([%%#])", "%1"):gsub("##", "#")
  etat = nil
  colorer(s)
  etat = nil
end

return otpy
