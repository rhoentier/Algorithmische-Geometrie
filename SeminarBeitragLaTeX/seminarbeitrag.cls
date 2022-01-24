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
\newcommand{\w}{$W()$ }
\renewcommand{\v}{$V()$ }
\newcommand{\cp}{$CP$ }
\newcommand{\cpi}{$CP_{i}$ }
\newcommand{\s}[1]{$S_{#1}$ }
\newcommand{\si}{$S_{i}$ }
\renewcommand{\pi}{$P_{i}$ }
\newcommand{\mprl}{P_{L}^{r}}
\newcommand{\prl}{$P_{L}^{r}$ }
\newcommand{\mpll}{P_{L}^{l}}
\newcommand{\pll}{$P_{L}^{l}$ }
\newcommand{\ord}{\textit{OrderPieces} }
\newcommand{\con}{\textit{ConvexDivide} }
\newcommand{\noncon}{\textit{NonConvexDivide} }
\newcommand{\daa}{\textit{DetachAndAssign} }
\newcommand{\cpn}{$CP_{1},...,CP_{n}$ }
\newcommand{\iton}{$i=1,...,n$ }
\newcommand{\ar}[1]{$Area(#1)$ }
\newcommand{\mar}[1]{Area(#1)}
\newcommand{\arreq}[1]{$AreaRequired(#1)$ }
\newcommand{\marreq}[1]{AreaRequired(#1)}
\newcommand{\pred}[1]{$PredPoly($#1$)$ }
\newcommand{\predl}[2]{$PredPoly($#1$, $#2$)$ }



\usepackage{datetime}
\date{\large\monthname~\the\year}

\addto\captionsenglish{\def\keywordsname{Keywords}}
\addto\captionsgerman{\def\keywordsname{Stichw\"orter}}
\addto\captionsngerman{\def\keywordsname{Stichw\"orter}}

\providecommand{\keywords}[1]
{\par\smallskip\noindent\normalsize{\sffamily\textbf{\keywordsname:}} #1\par
}
