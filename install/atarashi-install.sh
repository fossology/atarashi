#!/bin/bash

# Copyright 2018 Aman Jain (amanjain5221@gmail.com)
#
# SPDX-License-Identifier: GPL-2.0
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# Author: Aman Jain (amanjain5221@gmail.com)

# This script includes the installation of all pre-requisites
# for running atarashi project.

BASEDIR=$(dirname $0)

python_for_mac()
{
  which -s brew
  SUCCESS=$?
  if [[ $SUCCESS -ne 0 ]]
  then
    echo "You don't have brew. Installing brew ..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  else
    echo "Brew Found. Updating it ..."
    brew update 
  fi
  brew install python
}

echo "Determining the OS ..."
unameOut="$(uname -s)"
case "${unameOut}" in
  Linux*)
    operating_system=Linux;;
  Darwin*)
    operating_system=Mac;;
  *) 
    operating_system="UNKNOWN:${unameOut}"
esac

which python3
PYTHON=$?

which pip
PIP=$?

if [[ ( $PYTHON -eq 0 ) && ( $PIP -eq 0 ) ]]; then
  echo "Python 3 and pip is already installed"

elif [[ ( $PYTHON -eq 0 ) && ( $PIP -ne 0 ) ]]; then
  echo "Python 3 exists and pip doesnot exists"
  if [ $operating_system == "Linux" ]; then
    # python and pip install according to distro
    DISTRO=`lsb_release -is`
    echo "Detected Distro ... ${DISTRO}. Installing pip..."
    case "$DISTRO" in
      Debian|Ubuntu|LinuxMint)
        sudo apt-get -y install python-pip;;
      Fedora)
        sudo yum -y install python-pip;;
      RehHatEnterprise*|CentOS)
        sudo yum -y install python36u-pip
        sudo yum -y install python36u-devel;;
      *) echo "ERROR: distro not recognised, please fix and send a patch"; exit 1;;
    esac
  elif [ $operating_system == "Mac" ]; then
    # pip install in Mac
    python_for_mac
  fi

else
  echo "Python 3 not found"
  if [ $operating_system == "Linux" ]; then
    # python and pip install according to distro
    DISTRO=`lsb_release -is`
    echo "Detected Distro ... ${DISTRO}. Installing Python and pip..."
    case "$DISTRO" in
      Debian|Ubuntu|LinuxMint)
        sudo apt-get -y install python3
        sudo apt-get -y install python-pip;;
      Fedora)
        sudo yum -y install python3
        sudo yum -y install python-pip;;
      RehHatEnterprise*|CentOS)
        sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
        sudo yum -y install python36u
        sudo yum -y install python36u-pip
        sudo yum -y install python36u-devel;;
      *) echo "ERROR: distro not recognised, please fix and send a patch"; exit 1;;
    esac
  elif [ $operating_system == "Mac" ]; then
    # python install in Mac
    python_for_mac
  fi

fi

# Installs Code_comment from Git https://github.com/amanjain97/code_comment
echo "Installing Code_comment ..."
pip install --user -e git+https://github.com/amanjain97/code_comment#egg=code_comment
pip install --user -r $BASEDIR/../requirements.txt
