from emotion_detection import EmotionDetection

emotion_detection = EmotionDetection()
# (1.) photo sentiment analysis
emotion_detection.get_photo_emotion_dict()
emotion_detection.plot_emotion_trend()
# (2.) text sentiment analysis
emotion_detection.get_text_emotion_dict()
emotion_detection.plot_emotion_trend(mode = 'text')
# # (3.) text word cloud
# emotion_detection.get_month_data_dict()
# emotion_detection.write_month_data()
# emotion_detection.plot_emotion_trend(mode = 'text')