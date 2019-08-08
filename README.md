# Ezoo_play Project:

## Project Goal:
- Adding top songs for a list of artists. <br>
As Electric Zoo 2019 is around the corner, this project is ideated specifically for adding songs for EZoo 2019 artists.<br>
However, the code can be easily adapted to add top songs for any list of artists.

## Instructions:

1. Copy this repository:

  `git clone https://github.com/0ethel0zhang/ezoo_play.git`

(Optional) Create your own list of artists if EZoo 2019 isn't your cup of tea:
- save the list of artists in a text file under the path `data\artists.txt`

2. Create a virtual environment running the following command in command line (Replace the NAMEYOULIKE part with whatever name you want to call your virtual environment):

  `conda env create -f environment.yml -n NAMEYOULIKE`

3. Activate the environment using:

  `conda activate NAMEYOULIKE`

4. If you want to access your own spotify playlist. Create a .env file in the main directory with the following access information (use your own key and token):

  `export user_name = "whatever"`<br>
	`export client_id = "whatever"`<br>
	`export client_secret = "whatever"`<br>
	`export redirect_uri = "Whatever"`

5. To run the main program:

  `python src/play.py`
  
  Follow any instructions that is prompted in the command line. (The only one should be a spotify verification step that requires you to copy the address of the pop-up website.)
  
## Conclusion
After everything finished running, **Viola**, you have a playlist called "Electric Zoo 2019" with Top songs from all artists in your list!
