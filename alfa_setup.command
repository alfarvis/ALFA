#!/usr/bin/env bash
PS1='$ '
# Check if conda already installed
source ~/.bash_profile
conda info > /dev/null
if [ $? -eq 0 ]; then
  echo "Conda already installed"
  CONDA_INSTALLED=true
else
  CONDA_INSTALLED=false
fi

if [ $CONDA_INSTALLED = false ]; then
  echo "Installing Anaconda..."
  CURRENT_DIR=$PWD
  # Go to tmp
  cd /tmp

  # You can change what anaconda version you want at 
  # https://repo.continuum.io/archive/
  MACHINE_TYPE=`uname -m`
  if [ ${MACHINE_TYPE} == 'x86_64' ]; then
    # 64-bit stuff here
    FILE_NAME=Anaconda2-5.3.0-Linux-x86_64.sh
  else
    # 32-bit stuff here
    FILE_NAME=Anaconda2-5.3.0-Linux-x86.sh
  fi
  wget "https://repo.continuum.io/archive/$FILE_NAME"
  bash $FILE_NAME -b -p ~/anaconda
  echo 'export PATH="~/anaconda/bin:$PATH"' >> ~/.bash_profile

  # Refresh basically
  source ~/.bash_profile

  conda update conda

  conda info > /dev/null
  if [ $? -ne 0 ]; then
    echo "Failed to installed Anaconda"
    exit
  fi
  cd $CURRENT_DIR
fi
cd $HOME
rm -rf Alfa.app
mkdir -p Alfa.app/Contents/
cd Alfa.app/Contents
git clone https://garimellagowtham@github.com/garimellagowtham/Alfarvis MacOS
if [ $? -ne 0 ]; then
  echo "Failed to clone Alfa"
  exit
fi
cd MacOS
git checkout mac_installation
chmod +x alfa alfa_notebook.py alfa_gui.py alfa_terminal.py
conda env create -f environment.yaml
#if [ $? -ne 0 ]; then
#  echo "Failed to create environment"
#  exit
#fi
# Create a database in Home folder
mkdir $HOME/AlfaDatabase
cp ./Alfarvis/resources/* $HOME/AlfaDatabase/
# Add to path maynot be necessary
#echo 'export PATH="~/.Alfarvis:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
### Create ICONS
ORIGICON=./alfa.png
PROJECT=Alfa
ICONDIR=../Resources/$PROJECT.iconset

mkdir -p $ICONDIR

# Normal screen icons
for SIZE in 16 32 64 128 256 512; do
sips -z $SIZE $SIZE $ORIGICON --out $ICONDIR/icon_${SIZE}x${SIZE}.png ;
done

# Retina display icons
for SIZE in 32 64 256 512 1024; do
sips -z $SIZE $SIZE $ORIGICON --out $ICONDIR/icon_$(expr $SIZE / 2)x$(expr $SIZE / 2)@2x.png ;
done

# Make a multi-resolution Icon
iconutil -c icns -o $HOME/$PROJECT.app/Contents/Resources/$PROJECT.icns $ICONDIR
#rm -rf $ICONDIR #it is useless now
#########
