mkdir temp
wget -O temp/mediawiki.tar.gz http://releases.wikimedia.org/mediawiki/1.22/mediawiki-1.22.3.tar.gz
cd temp
tar xvzf mediawiki.tar.gz
sudo ln -s $(pwd)/mediawiki-1.22.3/ /var/www/w
chmod 777 mediawiki-1.22.3/mw-config/
cd ..
cp LocalSettings.php temp/mediawiki-1.22.3/
