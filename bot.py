import logging
import os

import concurrent.futures
from types import NoneType
from bs4 import BeautifulSoup
import requests
import pandas as pd
from random import random, randint
from dotenv import load_dotenv 
from slack_bolt import App 
from slack_bolt.adapter.socket_mode import SocketModeHandler 

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("APP_TOKEN")

app = App(token=SLACK_BOT_TOKEN)

#@app.event("app_mention")
def mention_handler(body, context, payload, options, say, event):
    say("Hello World!")

@app.event("message")
def message_handler(body, context, payload, options, say, event):
    pass

@app.event("app_mention")
def test(body, context, payload, options, say, event):
	pass	

#MAX_THREADS = 2

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'})

bestbuy_infolist = []



@app.command('/infoitem')
def info_item(body, ack, client, logger):
    logger.info(body)
    ack()
    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
	"type": "modal",
	"callback_id": "infoitem_menu",
	"title": {
		"type": "plain_text",
		"text": "Item Information",
		"emoji": False
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": False
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": False
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "my_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "my_action"
			},
			"label": {
				"type": "plain_text",
				"text": "Paste a bestbuy item link to recieve information!",
				"emoji": False
			}
		}
	]
	}
    )
    logger.info(res)


@app.view("infoitem_menu")
def infoitem_menu_answer(ack, body, logger):
	ack()
	logger.info(body["view"]["state"]["values"])
	infoitem_menu_text = body["view"]["state"]["values"]["my_block"]["my_action"]["value"]
	bestbuy_infolist.append(infoitem_menu_text)
	for links in bestbuy_infolist:
		url = requests.get(links, headers=HEADERS)
		soup = BeautifulSoup(url.content, 'lxml')
		itemz = soup.find("h1", attrs={'class':'heading-5 v-fw-regular'}).string.strip()
		valuez = soup.find("span", attrs={'class':'sr-only'}).contents[2]

		try:
			descriptionz = soup.find("div", attrs={'class':'html-fragment'}).string.strip()
		except:
			descriptiony = soup.select('div[class="product-description"]')
			descriptionz = ''
			for h in descriptiony:
				descriptionz += h.text
		else:
			descriptionz = soup.find("div", attrs={'class':'html-fragment'}).string.strip()
		
		try:
			quick_check_code = soup.find("button", attrs={'class':'c-button c-button-primary c-button-lg c-button-block c-button-icon c-button-icon-leading add-to-cart-button'})
			if "Add to Cart" in quick_check_code:
				quick_check = "Buy Now"
		except:
			quick_check = "Out of Stock"
		else:
			quick_check = "Buy Now"

		bestbuy_infolist.clear()

	app.client.chat_postMessage(channel="tommy_bot_testing", blocks=[
			{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": f"{itemz}",
				"emoji": False
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"{descriptionz}"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://cdn.vox-cdn.com/thumbor/Lf9aj9A_nn0uScv_yetBXFf8YAA=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/10806197/2018_rebrand_blog_logo_LEAD_ART.jpg",
				"alt_text": " "
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"The current listing price on Best Buy is ${valuez}"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": f"{quick_check}",
					"emoji": False
				},
				"value": "click_me_123",
				"action_id": "button-action",
				"url":  f"{infoitem_menu_text}"
			}
		}
	]
)


'''
def thread_rippin(x):
	threads = min(MAX_THREADS, len(story_urls))
	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:

'''

@app.command('/random')
def handle_command(body, ack, client, logger):
    logger.info(body)
    ack()
    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
	"type": "modal",
	"callback_id": "random_menu",
	"title": {
		"type": "plain_text",
		"text": "Random Image Generator",
		"emoji": False
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": False
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": False
	},
	"blocks": [
		{
			"type": "input",
			"block_id": "my_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "my_action"
			},
			"label": {
				"type": "plain_text",
				"text": "Type a single word to generate an Image!",
				"emoji": False
			}
		}
	]
	}
    )
    logger.info(res)

@app.view("random_menu")
def randon_menu_answer(ack, body, logger):
    ack()
    logger.info(body["view"]["state"]["values"])
    random_menu_text = body["view"]["state"]["values"]["my_block"]["my_action"]["value"]
    app.client.chat_postMessage(channel="tommy_bot_testing", blocks=[
			{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Random Image Generator",
				"emoji": False
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": f"You've requested an image of a {random_menu_text}",
				"emoji": False
			},
			"image_url": f"""https://source.unsplash.com/1600x900/?{{{random_menu_text}}}""",
			"alt_text": " "
		}
	]
)
        
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

