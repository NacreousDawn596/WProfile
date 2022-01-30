from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import json
import os


app = Flask(__name__)


@app.route("/WProfile/<Username>/<Languages>/<Description>")
def WProfile(Username, Languages, Description, image='R.jpg'):
	def ajout_des_bordures(im, radian=200):
	    rounded = Image.new('L', (radian * 2, radian * 2), 0)
	    draw = ImageDraw.Draw(rounded)
	    draw.ellipse((0, 0, radian * 2, radian * 2), fill=255)
	    new_img_with_borders = Image.new('L', im.size, "white")
	    w, h = im.size
	    new_img_with_borders.paste(rounded.crop((0, 0, radian, radian)), (0, 0))
	    new_img_with_borders.paste(rounded.crop((0, radian, radian, radian * 2)), (0, h - radian))
	    new_img_with_borders.paste(rounded.crop((radian, 0, radian * 2, radian)), (w - radian, 0))
	    new_img_with_borders.paste(rounded.crop((radian, radian, radian * 2, radian * 2)), (w - radian, h - radian))
	    im.putalpha(new_img_with_borders)
	    return im
	def Git(username=Username):
		git = os.popen(f'curl -H "Authorization: token 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" https://api.github.com/users/{username}').read()
		return json.loads(git)
	def saveimg(img,  username=Username):
		img.show()
		img.convert('RGB').save(f"{username}.jpeg","JPEG")
	img = Image.open(image)
	if len(Languages.split()) > 10:
		space = 150+43*len(Languages.split())
		W, H = (1200, 150+43*len(Languages.split()))
	else:
		W, H = (1200, 640)
	new_image = img.resize((W, H))
	DrawImage = ImageDraw.Draw(new_image)
	new_image = ajout_des_bordures(new_image)
	print("test2")
	font_title = ImageFont.truetype('font/Anonymous_Pro_B.ttf', 30)
	font_username = ImageFont.truetype('font/Anonymous_Pro_BI.ttf', 40)
	font_text = ImageFont.truetype('font/Anonymous_Pro.ttf', 25)
	print("test1")
	DrawImage.text((600-len(Username)*11.5, 50), Username, fill=(255, 255, 255), font=font_username)
	DrawImage.text((105, 150), "Languages", fill=(255, 255, 255), font=font_title)
	DrawImage.text((505, 150), "Description", fill=(255, 255, 255), font=font_title)
	DrawImage.text((915, 150), "Informations", fill=(255, 255, 255), font=font_title)
	for lang in range(len(Languages.split())):
		space = lang + 1
		DrawImage.text((175-int(len(Languages.split()[lang])/2)*14, 150+43*space), Languages.split()[lang], fill=(255, 255, 255), font=font_text)
	for char in range(len(Description)):
		if char%35 == 0:
			space = char/35
			DrawImage.text((565-len(Description[char-35:char])/2*11.5, 150+43*space), Description[char-35:char], fill=(255, 255, 255), font=font_text)
	times = int(len(Description)/35)
	space += 1
	DrawImage.text((600-int(len(Description[len(Description)-int(len(Description)-35*times)::])/2)*14, 150+43*space), f"-{Description[len(Description)-int(len(Description)-35*times)::]}", fill=(255, 255, 255), font=font_text)
	git = Git()
	print(git)
	DrawImage.text((1080-len(f"Followers: {git['followers']}")*11.5, 200), f"Followers: {git['followers']}", fill=(255, 255, 255), font=font_text)
	DrawImage.text((1080-len(f"Following: {git['following']}")*11.5, 243), f"Following: {git['following']}", fill=(255, 255, 255), font=font_text)
	DrawImage.text((1110-len(f"Repositories: {git['public_repos']}")*11.5, 286), f"Repositories: {git['public_repos']}", fill=(255, 255, 255), font=font_text)
	DrawImage.text((1150-len(f"Created at: {git['created_at'].split('T')[0]}")*11.5, 329), f"Created at: {git['created_at'].split('T')[0]}", fill=(255, 255, 255), font=font_text)
	DrawImage.text((1100-len(f"Hireable?: {git['hireable']}")*11.5, 372), f"Hireable?: {git['hireable']}", fill=(255, 255, 255), font=font_text)
	lang = {}
	fam_lang = os.popen(f'curl -H "Authorization: token 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" https://api.github.com/users/{Username}/repos').read()
	for idk in json.loads(fam_lang):
		try:
			lang[idk["language"]] += 1
		except:
			lang[idk["language"]] = 1
	DrawImage.text((1140-len(f"MMost used language: {sorted(lang.items(), key=lambda x: x[1], reverse=True)[0][0]}")*11.5, 415), f"Most used language: {sorted(lang.items(), key=lambda x: x[1], reverse=True)[0][0]}", fill=(255, 255, 255), font=font_text)
	saveimg(new_image)
	print('test')
	return send_file(f"/app/{Username}.jpeg", mimetype='image/jpeg')