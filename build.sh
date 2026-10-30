#!/bin/sh
# Genera index.html (página completa para el navegador, GitHub Pages y la pantalla de inicio) a partir de src/app.html.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  printf '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icons/icon-192.png">\n<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
  printf '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-title" content="Mi semana">\n<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
  printf '<meta name="theme-color" content="#EDF0F4" media="(prefers-color-scheme: light)">\n<meta name="theme-color" content="#0C141F" media="(prefers-color-scheme: dark)">\n'
  printf '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n'
  cat src/app.html
  printf '\n</body>\n</html>\n'
} > index.html
