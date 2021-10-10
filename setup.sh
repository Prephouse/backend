#!/usr/bin/env bash

which -s brew
if [[ $? != 0 ]] ; then
  /bin/bash "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

which -s git
if [[ $? != 0 ]] ; then
  brew install git
  export PATH="/usr/local/bin:${PATH}"
fi

brew install docker
brew install docker-compose
brew install postgresql

# etc=/Applications/Docker.app/Contents/Resources/etc
# ln -s $etc/docker.bash-completion "$(brew --prefix)"/etc/bash_completion.d/docker
# ln -s $etc/docker-compose.bash-completion "$(brew --prefix)"/etc/bash_completion.d/docker-compose
# if [ -f "$(brew --prefix)"/etc/bash_completion ]; then
#   . "$(brew --prefix)"/etc/bash_completion
# else
#   exit 1
# fi

echo 'Building docker image...'
docker-compose up
# curl localhost:5000
