def download_speaker_samples(speaker_id, 
                             output_dir="resources/voices/speaker_samples", 
                             model="ylacombe/cml-tts", 
                             lang="portuguese"):
    dataset = load_dataset(model, lang)
    os.makedirs(output_dir, exist_ok=True)
    
    for split_name in dataset.keys():
        split_data = dataset[split_name]
        speaker_samples = [
            sample for i, sample in enumerate(split_data) 
            if sample['speaker_id'] == speaker_id
        ]
        
        print(f"\Finded {len(speaker_samples)} speakers samples {speaker_id} no split {split_name}")

        for i, sample in enumerate(speaker_samples):
            audio_data = sample['audio']
            audio_array = audio_data['array']
            sampling_rate = audio_data['sampling_rate']
            
            output_filename = f"speaker_{speaker_id}_sample_{i}_{os.path.basename(audio_data['path'])}"
            output_path = os.path.join(output_dir, output_filename)
            
            sf.write(output_path, audio_array, sampling_rate)
            
            print(f"Sample number {i+1} saved on: {output_path}")
            print(f"Text: {sample['text']}")
            print(f"Duration: {sample['duration']:.2f} seconds")
            print("-" * 50)