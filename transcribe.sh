for file in $@; do 
    f=`basename $file`
    echo "Processing $f"
    ffmpeg -i $file -acodec pcm_s16le -ar 16000 $file.wav; 
    deepspeech --model ~/deepspeech/deepspeech-0.9.3-models.pbmm --scorer ~/deepspeech/deepspeech-0.9.3-models.scorer --audio $file.wav > $file.txt;
done

