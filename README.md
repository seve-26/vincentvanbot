# Vincent Van Bot 🎨

An app that will let you find your new favorite painting.
Try it on the [**web app**](https://vincentvanbot.com/) or chat with our [**Telegram bot**](https://t.me/vincentvan_bot).

## Features
- 📸 **Picture to painting**: the user takes a picture of something beautiful he/she sees, and uploads it to Vincent Van Bot. The app returns paintings that look similar to the picture
- 😍 **Painting recommender**: the user inputs the title of his/her favorite painting. The app returns paintings that looks similar to the selected one

## Behind the scenes
Data source: [Web Gallery of Art](https://www.wga.hu/database/download/index.html)

#### Techniques and tools:
- `Pandas` and `Numpy` for data wrangling
- `Pillow` for image preprocessing
- Google Vision API for image labeling
- `NearestNeighbors` (with Minkowski distance) from `scikit-learn` for image similarity
- `FastAPI` for building API
- `streamlit` and `uvicorn` to build and run web app
- `Docker` and Google Compute Engine for hosting API, web app and Telegram bot
- Google Cloud Platform to manage entire project


A visualization of the workflow of the two features below (slides showed to non-tech audience). 

<img src="https://user-images.githubusercontent.com/74202982/111287200-472d1600-8643-11eb-89fa-5f5d3c71fad2.png" alt="Picture to Painting" width="700"/>
<img src="https://user-images.githubusercontent.com/74202982/111287324-6461e480-8643-11eb-84df-893c4a7ae103.png" alt="Painting Recommender" width="700"/>


## Contributors
This is the final project for the completion of [Le Wagon's Data Science bootcamp](https://www.lewagon.com/data-science-course/full-time).

The project has been completed in less than two weeks by a team of 4 classmates:
- [Severo Bregante](https://github.com/seve-26)
- [Nikolay Podvorchan](https://github.com/rtnikki)
- [Julia Schmitt](https://github.com/JulSchmitt)
- [Mauritz von Lenthe](https://github.com/maulenthe)

Thanks a lot for your effort team!
