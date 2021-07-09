# Dathoven

[Dathoven](http://dathoven.s3-website.eu-west-3.amazonaws.com) is a computer-aided music composition system that tries to help music composers to explore different melodic ideas faster and easier, even on those days when it seems like inspiration is nowhere to be found!

Using data extracted from MIDI files a neural network with LSTMs was trained to generate original melodies. This melodies are suggested to the composer using a web app. 

## Abstract

All the information about the project is in the [Abstract document](https://github.com/Juanvr/Dathoven/blob/main/TFM%20-%20Abstract%20-%20Dathoven.pdf). 

## Notebooks
The easiest way to follow the different steps of the project is by reading the notebooks in colab: 

0. [Exploring MIDI](https://colab.research.google.com/github/Juanvr/Dathoven/blob/main/notebooks/0%20-%20Dathoven%20-%20Exploring%20MIDI.ipynb)
1. [Web Scraping MIDI](https://colab.research.google.com/github/Juanvr/Dathoven/blob/main/notebooks/1%20-%20Web%20Scraping%20MIDI.ipynb)
2. [Building the Data Set](https://colab.research.google.com/github/Juanvr/Dathoven/blob/main/notebooks/2%20-%20Building%20the%20Dataset.ipynb)
3. [Analysing and Cleaning the Data Set](https://colab.research.google.com/github/Juanvr/Dathoven/blob/main/notebooks/3%20-%20Analysing%20and%20Cleaning%20the%20Dataset.ipynb)
4. [Model](https://colab.research.google.com/github/Juanvr/Dathoven/blob/main/notebooks/4%20-%20Model.ipynb)

## Frontend

The frontend is in [this repo](https://github.com/Juanvr/Dathoven-frontend-react).

## Models

The final models are on the repo folder [tensorflowjs_models](https://github.com/Juanvr/Dathoven/tree/main/tensorflowjs_models)
