mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $port\n\n
enableCORS = false\n\
headless = false\n\
\n\
" > ~/.streamlit/config.toml