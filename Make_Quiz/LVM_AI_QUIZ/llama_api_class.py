
#---------------
import os
import base64
from openai import OpenAI
import cv2
import API_KEYS
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
# API key setup

class openai_bot():
  def __init__(self,model="llama3.2-90b-vision",details="high"):
          self.client = client = OpenAI(api_key = API_KEYS.llama_api_key,base_url = "https://api.llama-api.com")
          self.model=model
          self.details=details
  ###########################Question text image##########################################################################################
  def question_text_image(self,text,image):
# Getting the base64 string
      image_path="temp_im_llama.jpg"
      cv2.imwrite(image_path,image)
      #image_path = r"/home/deadcrow/Desktop/20230729_185654.jpg"
      base64_image = encode_image(image_path)


      for iii in range(400):

         try:
             response = self.client.chat.completions.create(
              model= "llama3.2-90b-vision",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": text,
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}",
                       "detail":  self.details#"high"# "low", "auto"
                      },
                    },
                  ],
                }
              ]#,temperature=0bad
            )
             answer = response.choices[0].message.content

             break
         except:
               import time
               print("error no response  from llama sleeping 4 seconds and retry")
               time.sleep(4)
               continue
      return answer

  ###########################Question text##########################################################################################
  def question_text(self, text):


      for iii in range(500):

          try:
              response = self.client.chat.completions.create(
                  model="llama3.2-90b-vision",
                  messages=[
                      {
                          "role": "user",
                          "content": [
                              {
                                  "type": "text",
                                  "text": text,
                              }
                          ],
                      }
                  ]
              )
              answer = response.choices[0].message.content

              break
          except:
              import time
              print("error no response from llama sleeping 4 seconds and retry")
              time.sleep(4)
              continue

      return answer
###########################Full questions############################################################################################

  def answer_question(self, image):
      # various
      queries = [
          # the queries will be given in this order the next query will be given only if the model will refuse to answer the previous one
          (
              "Which of the panels contain object with identical 3d shape  to the object in panel A. Your answer must come as a single letter"),

          (
              "Which of the panels contain object that is identical in 3d shape to the object in panel A. Your answer must come as a single letter: B,C,D"),
          (
              "Carefully analyze the image. In panel A, there is an object with a specific shape. Your task is to identify which other panel (B, C, or D) contains an object that"
              "\n1) Has the exact same 3d shape as the object in panel A."
              "\n2) Might Have a different orientation compared to the object in panel A."
              "\n3) Might have a different texture compared to the object in panel A."
              "Respond with ONLY the letter of the panel (B, C, or D) that meets all these criteria."),

          ("The image contain 4 panels (A,B,C,D). "
           "The each panel contain object. "
           "One of the panels C-D contain object that is identical in shape to the object in panel A."  # #but  have different  background"#, orientation and texture. "
           "Which panel is this? Your answer must be a single letter (B,C or D)")]

      # -----------------repeat queries until getting correct format of answr (b,c,d)
      for ii in range(len(queries)):
          all_text = "\n\n query: " + queries[ii] + "\n"  # use to record full interaction
          ky = self.question_text_image(queries[ii], image)
          all_text += str(ii) + ") response:  " + ky +"\n"

          if len(ky) > 1 or ky.lower() not in ['b', 'c', 'd']:
              ky = self.question_text("Take the following response and reduce it to a single letter:\n" + ky)
              all_text += str(ii) + ")Take the following response and reduce it to a single letter: response:  " + ky
              if len(ky) > 1:
                  if (" B" in ky) and (" C" not in ky) and (" D" not in ky): ky = "B"
                  if (" B" not in ky) and (" C" in ky) and (" D" not in ky): ky = "C"
                  if (" B" not in ky) and (" C" not in ky) and (" D" in ky): ky = "D"
                  all_text += str(ii) + ")Extracting answer" + str(ii)
          if len(ky) and (ky.lower() in ['b', 'c', 'd']):
              return ky, all_text