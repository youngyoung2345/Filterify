# Filterify : Playlist Filtering Based on Album Covers

### Summarization

많은 사람들이 음악 스트리밍 플랫폼을 통해 음악을 감상하지만, 플랫폼이 제공하는 자동 플레이리스트 생성 기능은 플레이리스트의 완성도 혹은 흐름(유기성)을 해치는 음원을 완전히 필터링하지 못한다는 한계가 존재합니다. 유튜브 뮤직(Youtube Musice)을 통해 자동으로 생성한, 10개의 음원으로 구성된 플레이리스트 5개에 대하여 43명을 대상으로 설문 조사를 진행한 결과, 각 플레이리스트마다 평균적으로 약 2~3곡이 해당 플레이리스트의 완성도 혹은 흐름(유기성)을 해치는 음원으로 선택받았습니다. **Filterify**는 앨범 커버 이미지를 활용하여, 앞서 논한 한계를 가지는 자동 플레이리스트 생성 기능을 보완하는 프로젝트입니다. 


### Code instruction
```
'convert_from_json_to_csv.py'
```

json 형식으로 저장된 Audio Feature를 csv 형식으로 변환하는 코드입니다. 

```
'predict_tone_theme_from_cover.py', 'predict_tone_theme_from_description.py'
```

앨범 커버 및 앨범 소개 기반으로 음원의 톤(Tone)과 테마(Theme)를 예측하는 코드입니다.

```
'embed_features.ipynb'
```

(1) 앨범 커버 및 앨범 소개 기반으로 예측한 음원의 톤(Tone)과 테마(Theme)에 대한 텍스트와 (2)앨범 커버 이미지를 CLIP Encoder를 사용하여 임베딩하는 코드입니다.

```
'Training.ipynb'
```

'embed_features.ipynb'를 통해 임베딩한 Visual Feature 및 Textual Feature를 활용하여 Audio Feature를 예측하는 Audio Feature Predictor를 학습 및 평가하는 코드입니다.

```
'Filtering.ipynb'
```

'Trainiing.ipynb'를 통해 학습 및 평가한 Audio Feature Predictor 및 Visual Feature, Textual Feature를 활용하여 주어진 플레이리스트에 대하여 필터링을 수행하는 코드입니다.


### Demo 

Demo Video는 다음 링크(https://drive.google.com/file/d/1v4uJHJidrJbzGLJ7ejlhmdaTHv9c3DdT/view)를 통해 확인하실 수 있습니다.


### Conclusion and Future Work

**Filterify**는 (1) 약 500곡의 국내 음원에 대하여 Audio Feature 및 앨범 커버 이미지, 앨범 소개 텍스트로 구성된 Dataset을 구축하고, (2) 해당 Dataset에 기반한 Visual Feature 및 Textual Feature를 활용하여 Audio Feature를 예측하는 Lightweight Audio Feature Predictor를 학습하였으며, (3) 이를 바탕으로 플레이리스트의 완성도 혹은 흐름(유기성)을 해치는 음원을 필터링하는 시스템을 구현한 **앨범 커버 기반 음악 필터링 프로젝트**입니다. 43명을 대상으로 진행한 설문 조사를 기반으로 정량적 평가를 진행하였을 뿐만 아니라 모달리티(Modality) 별 중요도를 분석함으로써, 앨범 커버를 통해 플레이리스트의 완성도 혹은 흐름(유기성)을 향상시킬 수 있음을 확인하였습니다. 향후 모델 구조 개선, 어플리케이션 개발 등을 통해 시스템의 정확도와 활용도를 더욱 높일 예정입니다.

* * *

**Results of Data Analysis Capstone Design at Kyung Hee University**

**Team Members**  

| Name   | Role                             | Email                     |
|--------|----------------------------------|---------------------------|
| 이하영 | Leader of Filterify Project Team | lhayoung9@khu.ac.kr       |
| 이건   | Member of Filterify Project Team | sslmyo24@gmail.com        |
| 손훈석 | Member of Filterify Project Team | shs0714@khu.ac.kr         |
