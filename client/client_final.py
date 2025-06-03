from app import App
import argparse


parser = argparse.ArgumentParser(description="My program description")


parser.add_argument('--broadcast', type=int, default=3030, help='Broadcast Port')
parser.add_argument('--sender', type=int, default=3031, help='Sender Port')

args = parser.parse_args()
    
app = App(args.broadcast,args.sender)
app.start()