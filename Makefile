all: phase1


phase1:
	# Check required config files are present and create them if not
	./src/utils/check_conf_files.sh

	# Prepare hybrid volume
	mkdir -p ./build/vol/
	./src/utils/make_vc_volume.sh

	./src/utils/generate_files.sh


phase2:
	mkdir -p export
	./src/utils/angecryption.sh

clean:
	rm -rf build

clean_all: clean
	- rm config/*iv
	- rm config/*key
