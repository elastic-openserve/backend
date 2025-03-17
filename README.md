# backend


"""
This is an Auto Ad Post Generator for a Brand's product.
 - Create a Trend Analysis Report for my Product's category. - The user has to give a Product Description mentioning the Product ID, Description and Motive of its ad. The Product ID is 'P001'. Our brand is ElecX, revolutionizing electric scooters. We are passionate about creating fast, eco-friendly, and commuter-friendly scooters. The new ElecX Pro targets urban mobility solutions worldwide. The output result is called trend-result which is in a JSON format.
 - Now generate extensive report for user traffic using different groupings based on Age, Demography, Gender, Month etc. using the the sitelog agent, good market analyst agent. The input is only a single string, PRODUCT_ID. In our case input is just P001. The output result is called sitelog-result which is in a JSON format.
 - Now you refine the sitelog-result to get the top 2 months, top age group and top 2 regions with the highest number of user interactions. Your input is the sitelog-result, a raw JSON format. The output result is called sitelog-result which is in a JSON format.
 - Now we have pass the trend-result and sitelog-refined-result to the script writer agent to generate a list of advertisement text scripts for the product based on the insights for each month, age group, and region. The input is the product description, trend-result, and sitelog-refined-result. The output result is called script-result which is in a JSON format.
 - Now we have to pass the script-result to the image generator agent to generate images for the advertisement text scripts. The input is the script-result. The output result is called image-script-result which is in a JSON format.
 - Now we have to pass the image-script-result to the audio agent to generate audio for the advertisement text scripts. The input is the image-script-result. The output result is called audio-script-result which is in a JSON format.
 - Now we have to pass the audio-script-result to the video agent to generate video for the advertisement text scripts. The input is the audio-script-result. The output result is called video-result which is in a JSON format.
 - Now we have to pass the video-result to the email agent to send the advertisement text scripts and audio and video to the user. The input is the video-result. The output result is called email-result which is in a JSON format.

 
Task of the agent:
1. trend_analyzer_agent
You are a marketing strategist helping a brand identify the most effective search terms for trend analysis. It receives a single input PRODUCT_DESCRIPTION. The output is Demography wise trend data for the product category.

2. site_log_agent
You are a good market analyst. Your job is to monitor the sitelogs based on a given PRODUCT_ID. You will generate a extensive report fior user traffic using different groupings based on Age, Demography, Gender, Month etc. It takes a single string only, PRODUCT_ID. Example input: 'P001'

3. site_log_refiner_agent
This agent is responsible for refining the sitelog-result to get the top 2 months, top age group and top 2 regions with the highest number of user interactions. The input is the sitelog-result, a raw JSON format. The output result is called sitelog-result which is in a JSON format.

4. script_writer_agent
This agent is responsible for generating advertisement text scripts for the product based on the insights for each month, age group, and region. The agent will receive the product description, trend-result, and sitelog-refined-result as input and generate a list of advertisement text scripts for the product. The output result is called script-result which is in a JSON format.
 
5. image_generator_agent
This agent is responsible for generating images for the advertisement text scripts. The agent will receive the script-result as input and generate images for the advertisement text scripts. The output result is called image-script-result which is in a JSON format.

6. audio_agent

This agent is responsible for generating audio for the advertisement text scripts. The agent will receive the image-script-result as input and generate audio for the advertisement text scripts. The output result is called audio-script-result which is in a JSON format.

7. video_agent

This agent is responsible for generating video for the advertisement text scripts. The agent will receive the audio-script-result as input and generate video for the advertisement text scripts. The output result is called video-result which is in a JSON format.

8. email_agent

This agent is responsible for sending the advertisement text scripts and audio and video to the user. The agent will receive the video-result as input and send the advertisement text scripts and audio to the user. The acknowledgement will be in the form of email-result which is in a JSON format.
"""