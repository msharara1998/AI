mkdir -p ~/.streamlit/

echo"\
[general]\n\
email= \"ralphztawil@hotmail.com\"\n
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
enableCORS=false\n]
port = $PORT\n\
" > ~/.streamlit/config.toml