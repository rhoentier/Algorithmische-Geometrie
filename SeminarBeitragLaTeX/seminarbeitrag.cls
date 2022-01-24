% !TEX encoding = UTF-8 Unicode
% seminarbeitrag.cls
% einspaltiges Format (zum zweispaltigen siehe seminarvorlage.cls)
% LG Kooperative Systeme, FernUni Hagen, Januar 2022

\NeedsTeXFormat{LaTeX2e}
\def\fileversion{V0.1}
\def\filedate{Jan 11, 2022}
\ProvidesClass{seminarbeitrag}[\filedate, \fileversion]
\LoadClass[twoside,10pt]{scrartcl}% Abgeleitet von scrartcl (KOMA)

% Fonts
\RequirePackage[T1]{fontenc} % Moderne Fonts, Trennung von Woertern mit Umlauten
\RequirePackage{lmodern} % Latin Modern
% Mathe
\RequirePackage{amssymb} % American Mathematical Society
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{latexsym}

\RequirePackage{babel}% automatische Sprachunterstuetzung, auch \addto

% Seitenformat, A4-Papier, Seitenzahlen
\RequirePackage[a4paper,left=3cm,right=3cm,top=2.5cm, bottom=3cm]{geometry}
\pagenumbering{arabic}
\pagestyle{empty}
\addto\maketitle{\thispagestyle{empty}}

% Bilder
\RequirePackage{graphicx} % \includegraphics
\RequirePackage{color}
\usepackage[margin=2em,font=normalsize,labelfont={sf,bf}]{caption} % Bildunterschriften
% Referenzen, Links
\RequirePackage[pdftex,pdfpagelabels=false]{hyperref}
\hypersetup{%
    bookmarksnumbered,
    pdfstartview={FitH},
    colorlinks,
    citecolor=blue,
    filecolor=blue,
    linkcolor=blue,
    urlcolor=blue,
    breaklinks=true,
}
\RequirePackage{cleveref}% bequeme Referenzen mit \cref
\RequirePackage{embrac}% Klammern nicht kursiv, () und []

% Kommandos
\newcommand{\ls}{$L_{s}$ }
\renewcommand{\le}{$L_{e}$ }
\renewcommand{\l}{$L$ }
\newcommand{\leins}{$L_{1}$ }
\newcommand{\lzwei}{$L_{2}$ }
\newcommand{\w}{$W()$ }
\renewcommand{\v}{$V()$ }
\newcommand{\cp}{$CP$ }
\newcommand{\cpi}{$CP_{i}$ }
\newcommand{\mcpi}{CP_{i}}
\newcommand{\s}[1]{$S_{#1}$ }
\newcommand{\si}{$S_{i}$ }
\renewcommand{\pi}{$P_{i}$ }
\newcommand{\mprl}{P_{L}^{r}}
\newcommand{\mcprl}{CP_{L}^{r}}
\newcommand{\cprleins}{$CP^{r}_{L_{1}}$}
\newcommand{\cprlzwei}{$CP^{r}_{L_{2}}$}
\newcommand{\prl}{$P_{L}^{r}$ }
\newcommand{\mpll}{P_{L}^{l}}
\newcommand{\mcpll}{CP_{L}^{l}}
\newcommand{\pll}{$P_{L}^{l}$ }
\newcommand{\ord}{\mbox{\textit{OrderPieces}} }
\newcommand{\con}{\mbox{\textit{ConvexDivide}} }
\newcommand{\noncon}{\mbox{\textit{NonConvexDivide}} }
\newcommand{\daa}{\mbox{\textit{DetachAndAssign}} }
\newcommand{\cpp}{$CP_{1},...,CP_{p}$ }
\newcommand{\iton}{$i=1,...,n$ }
\newcommand{\ar}[1]{$Area(#1)$ }
\newcommand{\mar}[1]{Area(#1)}
\newcommand{\arreq}[1]{$AreaRequired(#1)$ }
\newcommand{\marreq}[1]{AreaRequired(#1)}
\newcommand{\pred}[1]{$PredPoly(#1)$ }
\newcommand{\predl}[2]{$PredPoly(#1, #2)$ }
\newcommand{\next}[1]{$NextNeighbor(#1)$ }



\usepackage{datetime}
\date{\large\monthname~\the\year}

\addto\captionsenglish{\def\keywordsname{Keywords}}
\addto\captionsgerman{\def\keywordsname{Stichw\"orter}}
\addto\captionsngerman{\def\keywordsname{Stichw\"orter}}

\providecommand{\keywords}[1]
{\par\smallskip\noindent\normalsize{\sffamily\textbf{\keywordsname:}} #1\par
}
