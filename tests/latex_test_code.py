MWE = r"""
\documentclass{article}

\usepackage{graphicx}
\usepackage{tikz}

\newlength{\figurewidth}
\newlength{\matplatextmp}

\begin{document}

\setlength{\figurewidth}{\linewidth}
\input{figure.pdf_tex}

\end{document}
"""

TIKZEXTERNALIZE = r"""
\documentclass{article}

\usepackage{graphicx}
\usepackage{tikz}
\pgfrealjobname{document}

\newlength{\figurewidth}

\begin{document}

\setlength{\figurewidth}{\linewidth}
\input{figure.pdf_tex}

\end{document}
"""


