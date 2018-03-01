#!/bin/bash

function die() {
    echo $@
    exit
}

echo "Creating mp3 file..."
cp ./build/audio.mp3 ./build/mp3_file
python ./src/angecrypt.py -c ./build/hybrid -i ./build/mp3_file -o ./build/mp3_out -k ./config/mp3_key -a aes -p ./build/
python ./build/dec-mp3_file.py #|| die "Error while executing dec-mp3_file.py"
echo "Done!"

echo "Creating pdf file..."
cp ./build/score.pdf ./build/pdf_file
python ./src/angecrypt.py -c ./build/dec-mp3_file.mp3 -i ./build/pdf_file -o ./build/pdf_out -k ./config/pdf_key -a aes -p ./build/
python ./build/dec-pdf_file.py
echo "Done!"

echo "Creating png file..."
cp ./build/matryoshka.png ./build/png_file
python ./src/angecrypt.py -c ./build/dec-pdf_file.pdf -i ./build/png_file -o ./build/png_out -k ./config/png_key -a aes -p ./build/
python ./build/dec-png_file.py
echo "Done!"

sum="$(shasum ./build/dec-png_file.png | awk '{print $1}')"

cp ./build/dec-png_file.png ./export/$sum.png
tar cvzf ./export/matryoshkryption.tgz --directory ./export/ $sum.png
rm ./export/$sum.png

echo -e "\nThe output file to give to the challenger can be found in \`./export/\`"
