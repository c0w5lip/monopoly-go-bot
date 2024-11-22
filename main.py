import pyautogui
import pydirectinput
import glob
import pyscreeze
import PIL.Image
import pynput
import requests
import time


### FILL OUT THESE
webhook_url = "" # LEAVE THIS BLANK IF YOU DON'T GIVE A F
restart_interval = 1200
###




running = False
cache = {}


def send_screenshot(message):
	screenshot = pyautogui.screenshot()
	screenshot_path = "logs/screenshot.png"
	screenshot.save(screenshot_path)

	with open(screenshot_path, 'rb') as file:
		requests.post(
			webhook_url,
			data={'content': message},
			files={'file': (screenshot_path, file)}
		)


def sort_images(images):
	order = [
		"wins_1.png",
		"tap_to_claim.png",

		"shop_ping.png",

		"build_1.png",
		"build_2.png",
		"build_3.png",
		"build_4.png",
		"build_5.png",

		"roll.png",

		"go.png",
		"collect.png",
		"awesome.png",
		
		"spin.png",
		"start.png",
		"go_green.png",
		"close_red.png",
		"close_gray.png",
		"close_gray_2.png",
		"close_beige.png",
		"equip.png",
		"heist_card.png",
		"switch_opponent.png",
		"rewards.png"
	]
	
	return sorted(images, key=lambda x: {image: index for index, image in enumerate(order)}.get(x[0], float('inf')))


def on_key_press(key):
	global running
	if key == pynput.keyboard.Key.f2:
		running = not running
		print("[*] Started" if running else "[-] Stopped")


def setup_key_handler():
	listener = pynput.keyboard.Listener(on_press=on_key_press)
	listener.start()



def get_image(path):
	global cache
	image = cache.get(path)
	if image is None:
		image = cache[path] = PIL.Image.open(f"images/{path}")
	
	return image


def get_image_location(image):
	result = pyautogui.locateOnScreen(image, grayscale=False, confidence=0.65)
	if result is None:
		return None
	
	bottom_left_x = result.left
	bottom_left_y = result.top + result.height
	return pyscreeze.Point(bottom_left_x, bottom_left_y)


def click_image(image_path, image_location):
	print("[*] Clicking {} -> ({}, {})".format(image_path, image_location.x, image_location.y))
	pyautogui.moveTo(x=image_location.x, y=image_location.y, duration=0.2)
	pydirectinput.click()


def process_round(found_images):
	for image in sort_images(found_images):
		image_path, image_location = image

		go_image_location = get_image_location(get_image("go.png")) # needed for calculations
		build_image_location = get_image_location(get_image("build.png")) # needed for calculations
		
		if ((image_path == "wins_1.png") and
	  		build_image_location is not None and # Check if "go.png" is found
			image_location.x < build_image_location.x # So it doesn't click on "Friends" or "Build"
		):
			click_image(image_path, image_location)
			return
		
		if image_path == "shop_ping.png": # If we have a free gift
			click_image(image_path, image_location)
			

			time.sleep(1) # Wait for the shop to open

			free_gift_button = get_image_location(get_image("free.png"))
			if free_gift_button is not None:
				click_image("free.png", free_gift_button)
			
			return


		if ((image_path == "build_1.png" or
	  		image_path == "build_2.png" or
			image_path == "build_3.png" or
			image_path == "build_4.png" or
			image_path == "build_5.png") and
			go_image_location is not None and # Check if "go.png" is found
			image_location.x < go_image_location.x # so it doesn't click on "Frends"
		):
			print("[*] Entering build menu...")
			click_image(image_path, image_location)
			
			time.sleep(2) # Wait for the build menu to open

			close_beige = get_image_location(get_image("close_beige.png"))

			if close_beige is None:
				print("[!] Couldn't enter the menu")
				return
			
			keep_building_counter = 0
			for build_card in [pyscreeze.Point(x_offset, close_beige.y - 150) for x_offset in range(close_beige.x - (2*115), close_beige.x + (3*115), 115)]:
				if keep_building_counter >= 5:
					break

				click_image("<build card>", build_card)
				time.sleep(1) # Wait for the "keep building" pop-up to show up

				if get_image_location(get_image("keep_building.png")):
					keep_building_counter += 1
					close_red = get_image_location(get_image("close_red.png"))
					click_image("close_red.png", close_red)
					time.sleep(1) # Wait for the "keep building" pop-up to close
			
			return
		

		if (image_path == "tap_to_claim.png" or
			image_path == "go.png" or
	  		image_path == "collect.png" or
			image_path == "awesome.png" or
			image_path == "roll.png" or
			image_path == "spin.png" or
			image_path == "start.png" or
			image_path == "go_green.png" or
			image_path == "close_red.png" or
			image_path == "close_gray.png" or
			image_path == "close_gray_2.png" or
			image_path == "equip.png" or
			image_path == "rewards.png" or

			image_path == "heist_card.png"
		):
			click_image(image_path, image_location)
			return


		if image_path == "switch_opponent.png":
			print(f"[*] Fuzzing for targets...")

			for x in range(image_location.x, image_location.x + 400, 100):
				for y in range(image_location.y - 100, image_location.y - 800, -100):
					pyautogui.moveTo(x=x, y=y, duration=0.2)
					pydirectinput.click()

			return
		
		if image_path == "close_beige.png":
			click_image(image_path, image_location)
			return

		print("[!] Behaviour regarding '{}' is undefined; skipping...".format(image_path))



def restart_application():
	bluestacks_show_applications = get_image_location(get_image("utils/bluestacks_show_applications_low_quality.png"))
	click_image("utils/bluestacks_show_applications_low_quality.png", bluestacks_show_applications)

	pyautogui.moveTo(1100, 800)
	time.sleep(2)

	pyautogui.mouseDown()
	pyautogui.dragTo(1100, 200, duration=0.5)
	pyautogui.mouseUp()

	time.sleep(4)

	monopoly_go = get_image_location(get_image("utils/monopoly_go.png"))
	click_image("utils/monopoly_go.png", monopoly_go)

	time.sleep(30) # Wait for the application to restart



def play_as_guest_bypass():
	play_as_guest = get_image_location(get_image("menu/play_as_guest.png"))
	if play_as_guest is not None:
		click_image("menu/play_as_guest.png", play_as_guest)

		time.sleep(1)

		click_image("menu/play_as_guest_2.png", get_image_location(get_image("menu/play_as_guest_2.png")))


if __name__ == "__main__":
	setup_key_handler()
	print("[...] Press F2 to start the bot")
	
	last_restart_time = 0  # Timestamp of the last application restart

	while True:
		if not running:
			continue

		current_time = time.time()

		# Restart the application if the interval has passed
		if current_time - last_restart_time >= restart_interval:
			send_screenshot("`[*] Before restart`")
			restart_application()
			print("[!] Couldn't restart the application")

			play_as_guest_bypass()
			send_screenshot("`[*] After restart`")
			last_restart_time = current_time
		
		print()
		print("[*] New round")

		found_images = [] # (image_path, location)
		for image_path in glob.glob(pathname="*.png", root_dir="images"):
			if not running:
				continue

			image_location = get_image_location(get_image(image_path))
			if image_location is not None:
				print("[+] Found '{}' @ ({}, {})".format(image_path, image_location.x, image_location.y))
				found_images.append((image_path, image_location))
		
		if not running:
			continue
		
		if len(found_images) >= 1:
			print("[*] Processing round...")
			process_round(found_images)
		else:
			print("[!] Couldn't find any image")
