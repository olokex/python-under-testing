import subprocess
import argparse
import sys    
import os


"""
reactions = [
		":necktie:", ":black_joker:", ":smirk:", ":monorail:", ":slot_machine:", "thinking", ":grinning:", 
		":grimacing:", ":grin:", ":joy:", ":smiley:", ":smile:", ":sweat_smile:", ":laughing:", ":innocent:", 
		":wink:", ":sparkler:", ":cowboy:", ":jack_o_lantern:", ":owl:", ":tea:", ":birthday:", ":egg:", 
		":rugby_football:", ":running_shirt_with_sash:", ":goal:", ":mountain_cableway:", ":beach:", 
		":bridge_at_night:", ":calling:", ":wastebasket:", ":candle:", ":paperclip:", ":virgo:", ":ab:", 
		":passport_control:", ":speaker:", ":black_heart:", ":eye_in_speech_bubble:", ":pray::skin-tone-5:", 
		":spy::skin-tone-5:", ":flushed:", ":robot:", ":information_desk_person::skin-tone-5:", ":kiss:", 
		":dark_sunglasses:", ":frog:", ":rabbit2:", ":full_moon_with_face:", ":droplet:", ":cucumber:", 
		":performing_arts:", ":tickets:", ":fuelpump:", ":deciduous_tree:", ":clap::skin-tone-5:", 
		":scream_cat:", ":smiling_imp:", ":elephant:", ":zap:", ":cloud:", ":squid:", ":space_invader:", 
		":diamonds:", ':sunglasses:', ':ghost:', ':bow::skin-tone-5:', ':boot:', ':nauseated_face:',
		':fingers_crossed::skin-tone-5:', ':lying_face:', ':panda_face:', ':koala:', ':dash:', 
		':four_leaf_clover:', ':cooking:', ':fried_shrimp:', ':rice_ball:', ':pizza:', ':bread:', 
		':champagne_glass:', ':canoe:', ':european_castle:', ':anchor:', ':triangular_ruler:', 
		':yin_yang:', ':peace:', ':hotsprings:', ':fleur_de_lis:', ':koko:', ':registered:', ':top:', 
		':black_medium_small_square:', ':busts_in_silhouette:', ':tv:', ':diamonds:', ':question:', 
		':two_hearts:', ':wavy_dash:'
	]

chars = [
		"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", 
		"p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D",
		"E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
		"T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", 
		"8", "9", " ", "'", 'ú', 'ů', 'ý', 'ž', 'á', 'č', 'ď', 'é', 'ě', 'í', 'ň', 
		'ó', 'ř', 'š', 'ť', 'Ú', 'Ů', 'Ý', 'Ž', 'Á', 'Č', 'Ď', 'É', 'Ě', 'Í', 'Ň', 
		'Ó', 'Ř', 'Š', 'Ť', ",", ".", "?", ":", "-"
	]
"""
char_key = {
	'a': ':necktie:', 'b': ':black_joker:', 'c': ':smirk:', 'd': ':monorail:', 'e': ':slot_machine:', 'f': ':thinking:',
	'g': ':grinning:', 'h': ':grimacing:', 'i': ':grin:', 'j': ':joy:', 'k': ':smiley:', 'l': ':smile:', 
	'm': ':sweat_smile:', 'n': ':laughing:', 'o': ':innocent:', 'p': ':wink:', 'q': ':sparkler:', 'r': ':cowboy:',
	's': ':jack_o_lantern:', 't': ':owl:', 'u': ':tea:', 'v': ':birthday:', 'w': ':egg:', 'x': ':rugby_football:', 
	'y': ':running_shirt_with_sash:', 'z': ':goal:', 'A': ':mountain_cableway:', 'B': ':beach:', 'C': ':bridge_at_night:',
	'D': ':calling:', 'E': ':wastebasket:', 'F': ':candle:', 'G': ':paperclip:', 'H': ':virgo:', 'I': ':ab:', 
	'J': ':passport_control:', 'K': ':speaker:', 'L': ':black_heart:', 'M': ':eye_in_speech_bubble:', 
	'N': ':pray::skin-tone-5:', 'O': ':spy::skin-tone-5:', 'P': ':flushed:', 'Q': ':robot:', 
	'R': ':information_desk_person::skin-tone-5:', 'S': ':kiss:', 'T': ':dark_sunglasses:', 'U': ':frog:', 
	'V': ':rabbit2:', 'W': ':full_moon_with_face:', 'X': ':droplet:', 'Y': ':cucumber:', 'Z': ':performing_arts:', 
	'0': ':tickets:', '1': ':fuelpump:', '2': ':deciduous_tree:', '3': ':clap::skin-tone-5:', '4': ':scream_cat:', 
	'5': ':smiling_imp:', '6': ':elephant:', '7': ':zap:', '8': ':cloud:', '9': ':squid:', ' ': ':space_invader:', 
	"'": ':diamonds:', 'ú': ':sunglasses:', 'ů': ':ghost:', 'ý': ':bow::skin-tone-5:', 'ž': ':boot:', 
	'á': ':nauseated_face:', 'č': ':fingers_crossed::skin-tone-5:', 'ď': ':lying_face:', 'é': ':panda_face:', 
	'ě': ':koala:', 'í': ':dash:', 'ň': ':four_leaf_clover:', 'ó': ':cooking:', 'ř': ':fried_shrimp:', 'š': ':rice_ball:', 
	'ť': ':pizza:', 'Ú': ':bread:', 'Ů': ':champagne_glass:', 'Ý': ':canoe:', 'Ž': ':european_castle:', 'Á': ':anchor:', 
	'Č': ':triangular_ruler:', 'Ď': ':yin_yang:', 'É': ':peace:', 'Ě': ':hotsprings:', 'Í': ':fleur_de_lis:', 'Ň': ':koko:', 
	'Ó': ':registered:', 'Ř': ':top:', 'Š': ':black_medium_small_square:', 'Ť': ':busts_in_silhouette:', 
	',': ':tv:', '.': ':diamonds:', '?': ':question:', ':': ':two_hearts:', '-': ':wavy_dash:', '_': ':upside_down:'
}

react_key = {
	':necktie:': 'a', ':black_joker:': 'b', ':smirk:': 'c', ':monorail:': 'd', ':slot_machine:': 'e', ':thinking:': 'f', 
	':grinning:': 'g', ':grimacing:': 'h', ':grin:': 'i', ':joy:': 'j', ':smiley:': 'k', ':smile:': 'l', ':sweat_smile:': 'm', 
	':laughing:': 'n', ':innocent:': 'o', ':wink:': 'p', ':sparkler:': 'q', ':cowboy:': 'r', ':jack_o_lantern:': 's', ':owl:': 't', 
	':tea:': 'u', ':birthday:': 'v', ':egg:': 'w', ':rugby_football:': 'x', ':running_shirt_with_sash:': 'y', ':goal:': 'z', 
	':mountain_cableway:': 'A', ':beach:': 'B', ':bridge_at_night:': 'C', ':calling:': 'D', ':wastebasket:': 'E', ':candle:': 'F', 
	':paperclip:': 'G', ':virgo:': 'H', ':ab:': 'I', ':passport_control:': 'J', ':speaker:': 'K', ':black_heart:': 'L', 
	':eye_in_speech_bubble:': 'M', ':pray::skin-tone-5:': 'N', ':spy::skin-tone-5:': 'O', ':flushed:': 'P', ':robot:': 'Q', 
	':information_desk_person::skin-tone-5:': 'R', ':kiss:': 'S', ':dark_sunglasses:': 'T', ':frog:': 'U', ':rabbit2:': 'V', 
	':full_moon_with_face:': 'W', ':droplet:': 'X', ':cucumber:': 'Y', ':performing_arts:': 'Z', ':tickets:': '0', ':fuelpump:': '1', 
	':deciduous_tree:': '2', ':clap::skin-tone-5:': '3', ':scream_cat:': '4', ':smiling_imp:': '5', ':elephant:': '6', ':zap:': '7', 
	':cloud:': '8', ':squid:': '9', ':space_invader:': ' ', ':diamonds:': '.', ':sunglasses:': 'ú', ':ghost:': 'ů', 
	':bow::skin-tone-5:': 'ý', ':boot:': 'ž', ':nauseated_face:': 'á', ':fingers_crossed::skin-tone-5:': 'č', ':lying_face:': 'ď', 
	':panda_face:': 'é', ':koala:': 'ě', ':dash:': 'í', ':four_leaf_clover:': 'ň', ':cooking:': 'ó', ':fried_shrimp:': 'ř', 
	':rice_ball:': 'š', ':pizza:': 'ť', ':bread:': 'Ú', ':champagne_glass:': 'Ů', ':canoe:': 'Ý', ':european_castle:': 'Ž', 
	':anchor:': 'Á', ':triangular_ruler:': 'Č', ':yin_yang:': 'Ď', ':peace:': 'É', ':hotsprings:': 'Ě', ':fleur_de_lis:': 'Í', 
	':koko:': 'Ň', ':registered:': 'Ó', ':top:': 'Ř', ':black_medium_small_square:': 'Š', ':busts_in_silhouette:': 'Ť', ':tv:': ',', 
	':question:': '?', ':two_hearts:': ':', ':wavy_dash:': '-', ':upside_down:': '_'
}

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def encode(words):
	output_text = ""
	tmp_text = ""

	for each in words:
		for char in each:
			try:
				tmp_text += char_key[char]
			except KeyError:
				tmp_text += " CHYBA {} ".format(char)

		if (len(tmp_text) + len(output_text)) < 2000:
			output_text += tmp_text
			tmp_text = ""
		else:
			print(output_text)
			output_text = ""
			output_text += tmp_text
			tmp_text = ""
		
		# if len(words) != 1:
		# 	tmp_text = char_key[" "] + tmp_text

		if output_text[:len(char_key[" "]) * -1] != char_key[" "]:
			tmp_text += char_key[" "]

			#str replace

	copy2clip(output_text)

def decode(text):
	for each in react_key:
		try:
			text = text.replace(each, react_key[each])
		except KeyError:
			print("chyba")
	copy2clip(text)

# choice = input("Code - c | d - Decode ").upper().strip()
# text = input("Insert text for translation: ").strip()
# 
# if choice == "C":
# 	code(text.split(" "))
# elif choice == "D":
# 	decode(text)
# else:
# 	print("you have forgot to select")
# 
# print("Done")

file_name = os.path.basename(sys.argv[0])

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(1)

parser = MyParser(description='Example of use: {} -e lorem ipsum'.format(file_name))
group = parser.add_mutually_exclusive_group()
group.add_argument("-e", "--encode", help="Encode text into discord emoji", action="store_true", dest="encode")
group.add_argument("-d", "--decode", help="Decode discord emoji into text", action="store_true", dest="decode")
parser.add_argument("text", help="Insert text", type=str)
args = parser.parse_args()

if args.decode:
	decode(args.text.strip())
elif args.encode:
	encode(args.text.strip())
else:
	parser.print_help()