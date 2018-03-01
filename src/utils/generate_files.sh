#!/bin/bash


function die() {
    echo $@
    exit
}

# hybrid vc volume / mp4 file
python ./src/mp42HV.py ./assets/video.mp4 ./build/vc_volume ./build/hybrid
./src/utils/embed_2nd_flag.sh

# png file
python ./src/gen_t2m_dict.py -o ./build/dict_t2m -e ./build/dict_m2t.txt
python ./src/insert_lsb.py --text ./config/png_key --cover ./assets/matryoshka.png --output ./build/matryoshka_1.png --colors g --visual --asbytes --prefix "key: "
python ./src/insert_lsb.py --text ./config/png_iv --cover ./build/matryoshka_1.png --output ./build/matryoshka_2.png --colors b --visual --asbytes --prefix "iv: "
python ./src/insert_lsb.py --text ./build/dict_m2t.txt --cover ./build/matryoshka_2.png --output ./build/matryoshka.png --colors rgb
rm ./build/matryoshka_*


# pdf file
python ./src/utils/gen_pdf_text.py --template ./config/pdf_template --output ./build/pdf_text
echo -n "THCon 2018 - $(cat ./config/vc_passphrase | base64)" > ./build/pdf_tagline
python ./src/generate_music_score.py --input ./build/pdf_text --output ./build/score.ly --dict ./build/dict_t2m --title Stegophony --tagline ./build/pdf_tagline
lilypond -o ./build/score ./build/score.ly || die "You must install lilypond in order to build the challenge."


# mp3 file
python ./src/text_to_morse.py -i ./config/mp3_key -o ./build/morse.mp3 --samples ./assets/samples/ --asbytes --prefix "key "
python ./src/text_to_pic.py -i ./config/mp3_iv -o ./build/spectro.png --asbytes --prefix "iv: "
# The next step takes a while to complete (about 7min)
python ./src/spectrology/spectrology.py -o ./build/spectro.wav -m 0 -M 8000 ./build/spectro.png


echo -e "\nNext step:"
echo -e "\t open ./build/spectro.wav in Audacity"
echo -e "\t File > Import > browse to ./build/morse.mp3"
echo -e "\t Select all, then Tracks > Mix > Mix and Render"
echo -e "\t File > Export > Export as MP3 > export as ./build/audio.mp3"
echo -e "\nYou can now proceed to the second building phase by running \`make phase2\`"

