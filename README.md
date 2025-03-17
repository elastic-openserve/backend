
## How to run locally 

1. **Create the environment file**  
   Copy the `.env.example` file and rename it to `.env`. Adjust the environment variables as needed.

2. **Install dependencies and Run**  
   ```bash
   brew install ffmpeg
   pip install -r requirements.txt
   python3 wsgi.py
   ```
3. *** Tunneling ***
   ```bash
   ngrok http 7378
   ```

##How to use the Openserv platform to integrate these agents:
1. First of all we go the the Add Agent section and we fill in the form. For agent endpoint either use your local setup (as described above) or you can use the web app we have deployed for demo. Repeat the same for all the agents with the agent task description given below.
![Screenshot 2025-03-17 at 2 06 03 PM](https://github.com/user-attachments/assets/b71117f5-6c0a-41e9-acad-2c59cf69aec3)
2. Then go to each agent and click on generate secret key option. Copy the secret key and set it in the .env file as mentioned in the steps above. Repeat this for all the agents.
![Screenshot 2025-03-17 at 2 06 30 PM](https://github.com/user-attachments/assets/98d883ae-be64-4261-a28c-97adaf7cd046)
3. Then go to projects and create new project with the project description given below.
![Screenshot 2025-03-17 at 2 07 20 PM](https://github.com/user-attachments/assets/c4d05cfb-6dde-4a8c-843d-bef2d131e2c8)
4. In the select team, add all the agents you made in previous step.
![Screenshot 2025-03-17 at 2 07 33 PM](https://github.com/user-attachments/assets/3262323a-f94c-45a4-b2fd-8c6f21be5042)
5. Once project is created, approve the plan to make the project run.
![Screenshot 2025-03-17 at 2 08 00 PM](https://github.com/user-attachments/assets/a745b465-5cbd-45e0-91a2-a0fc5746bfcb)
6. Once it finishes running, you must have the output in your email!
   ![Screenshot 2025-03-17 at 2 10 16 PM](https://github.com/user-attachments/assets/740f8723-e1de-4b5e-ac83-51b19f8fde29)![Screenshot 2025-03-17 at 2 10 42 PM](https://github.com/user-attachments/assets/e1ab8e62-12fe-4db4-b6bd-765fbdac2766)![Screenshot 2025-03-17 at 2 10 57 PM](https://github.com/user-attachments/assets/170f74c6-4860-460c-90fc-ccfa7f28d0e2)



## This is a sample project description

This is an Auto Ad Post Generator for a Brand's product.
 - Create a Trend Analysis Report for my Product's category. - The user has to give a Product Description mentioning the Product ID, Description and Motive of its ad. The Product ID is 'P001'. Our brand is ElecX, revolutionizing electric scooters. We are passionate about creating fast, eco-friendly, and commuter-friendly scooters. The new ElecX Pro targets urban mobility solutions worldwide. The output result is called trend-result which is in a JSON format.
 - Now generate extensive report for user traffic using different groupings based on Age, Demography, Gender, Month etc. using the the sitelog agent, good market analyst agent. The input is only a single string, PRODUCT_ID. In our case input is just P001. The output result is called sitelog-result which is in a JSON format.
 - Now you refine the sitelog-result to get the top 2 months, top age group and top 2 regions with the highest number of user interactions. Your input is the sitelog-result, a raw JSON format. The output result is called sitelog-result which is in a JSON format.
 - Now we have pass the trend-result and sitelog-refined-result to the script writer agent to generate a list of advertisement text scripts for the product based on the insights for each month, age group, and region. The input is the product description, trend-result, and sitelog-refined-result. The output result is called script-result which is in a JSON format.
 - Now we have to pass the script-result to the image generator agent to generate images for the advertisement text scripts. The input is the script-result. The output result is called image-script-result which is in a JSON format.
 - Now we have to pass the image-script-result to the audio agent to generate audio for the advertisement text scripts. The input is the image-script-result. The output result is called audio-script-result which is in a JSON format.
 - Now we have to pass the audio-script-result to the video agent to generate video for the advertisement text scripts. The input is the audio-script-result. The output result is called video-result which is in a JSON format.
 - Now we have to pass the video-result to the email agent to send the advertisement text scripts and audio and video to the user. The input is the video-result. The output result is called email-result which is in a JSON format.

## Task of the agent:

1. trend_analyzer_agent

You are a marketing strategist helping a brand identify the most effective search terms for trend analysis. It receives a single input PRODUCT_DESCRIPTION. The output is Demography wise trend data for the product category.
Url: https://0e1c-171-50-207-252.ngrok-free.app/trend-analyzer

2. site_log_agent

You are a good market analyst. Your job is to monitor the sitelogs based on a given PRODUCT_ID. You will generate a extensive report fior user traffic using different groupings based on Age, Demography, Gender, Month etc. It takes a single string only, PRODUCT_ID. Example input: 'P001'
Url: https://0e1c-171-50-207-252.ngrok-free.app/site-log-agent

3. site_log_refiner_agent

This agent is responsible for refining the sitelog-result to get the top 2 months, top age group and top 2 regions with the highest number of user interactions. The input is the sitelog-result, a raw JSON format. The output result is called sitelog-result which is in a JSON format.
Url: https://0e1c-171-50-207-252.ngrok-free.app/site-log-refiner-agent

4. script_writer_agent

This agent is responsible for generating advertisement text scripts for the product based on the insights for each month, age group, and region. The agent will receive the product description, trend-result, and sitelog-refined-result as input and generate a list of advertisement text scripts for the product. The output result is called script-result which is in a JSON format.
Url: https://0e1c-171-50-207-252.ngrok-free.app/script-writer-agent 

5. iamge_generator_agent

This agent is responsible for generating images for the advertisement text scripts. The agent will receive the script-result as input and generate images for the advertisement text scripts. The output result is called image-script-result which is in a JSON format.
Url: https://0e1c-171-50-207-252.ngrok-free.app/image-generator-agent

6. audio_agent

This agent is responsible for generating audio for the advertisement text scripts. The agent will receive the image-script-result as input and generate audio for the advertisement text scripts. The output result is called audio-script-result which is in a JSON format.
Url: https://0e1c-171-50-207-252.ngrok-free.app/audio-agent

7. video_agent

This agent is responsible for generating video for the advertisement text scripts. The agent will receive the audio-script-result as input and generate video for the advertisement text scripts. The output result is called video-result which is in a JSON format.
Url: https://0e1c-171-50-207-252.ngrok-free.app/video-agent

8. email_agent
This agent is responsible for sending the advertisement text scripts and audio to the user. The agent will receive the audio-script-result as input and send the advertisement text scripts and audio to the user. The acknowledgement will be in the form of email-result which is in a JSON format.
Url: https://0e1c-171-50-207-252.ngrok-free.app/email-agent
