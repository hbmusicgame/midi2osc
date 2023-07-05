import pygame.midi
import argparse

from pythonosc import udp_client

pygame.init()
pygame.midi.init()

#入力MIDIデバイスの指定
input_id = pygame.midi.get_default_input_id()

#OSC通信のポート番号とIPアドレスを指定
OSC_PortNum = 9000
OSC_IPAdress= "127.0.0.1"

print("input MIDI:%d" % input_id)
i = pygame.midi.Input(input_id)
print("Port: " + str(OSC_PortNum))
print("IP Adress: " + str(OSC_IPAdress))
print ("starting")
#print ("full midi_events:[[[status,data1,data2,data3],timestamp],...]")

going = True

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default=OSC_IPAdress,
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=OSC_PortNum,
      help="The port the OSC server is listening on")
  args = parser.parse_args()
  client = udp_client.SimpleUDPClient(args.ip, args.port)


#ログの表示、OSC送信
while going:
    if i.poll():
        midi_events = i.read(10)
        # print ("full midi_events:" + str(midi_events))
        #print (str(midi_events[0][0][0]))
        OnOff = float(midi_events[0][0][0])
        if OnOff == 144:
            print("NoteOn ", end = ", ")
        elif OnOff == 128:
            print("NoteOff", end = ", ")
        elif OnOff == 224:
            print("PitchBend", end = ", ")
        elif OnOff == 176:
            print("Modulation", end = ", ")
        else:
            print("Other", end = ", ")
        
        note = float(midi_events[0][0][1])
        print("NoteNum: " + str(note), end = ", ")

        vel = float(midi_events[0][0][2])
        print("Velocity: " + str(vel))

        client.send_message("/midi", [OnOff, note, vel])

i.close()
pygame.midi.quit()
pygame.quit()
exit()