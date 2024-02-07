import tkinter as tk
from scraper import Scraper
import asyncio
import json, os
import collections
from nlp_model.ner import NER
from nlp_model.summarize import Summarizer
from nlp_model.topic_model import *
# https://finance.yahoo.com/news/apple-stock-buybacks-are-still-in-full-swing-and-thats-good-news-for-warren-buffett-221513294.html
# https://www.foxbusiness.com/retail/multiple-walmart-stores-new-york-incidents-credit-card-skimmers-july
# https://www.amazon.com/exec/obidos/subst/home/home.html

class Application(tk.Frame):
    def __init__(self, master=None, loop=None):
        super().__init__(master)
        self.master = master
        self.loop = loop
        self.grid(sticky="nsew")
        self.urls = set()
        self.create_widgets()
        self.scraper = Scraper()
        self.pages = []
        self.process_data = collections.defaultdict(list)
        self.ner = NER()
        self.summarizer = Summarizer()
        self.process_status_code = 0
        
    def create_widgets(self): 
        # scraping frame
        frame1 = tk.Frame(self.master)
        frame1.grid(row=0, column=0, sticky="nsew")
        
        left_frame = tk.Frame(frame1)
        left_frame.grid(row=0, column=0, sticky="nsew")
        
        self.label = tk.Label(left_frame, text="Article Summarizer", font=("Comic Sans MS", 20))
        self.label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
        self.scrollbar = tk.Scrollbar(left_frame)
        self.output = tk.Text(left_frame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=2, rowspan=10, sticky="nsew")
        self.output.grid(row=0, column=1, rowspan=10, sticky="nsew")
        self.scrollbar.config(command=self.output.yview)
        self.output.config(state="disabled")

        self.url_entry = tk.Entry(left_frame)
        self.url_entry.insert(0, "Enter the Article URL:")
        self.url_entry.config(fg="grey")
        self.url_entry.bind("<FocusIn>", self.clearPlaceholder)
        self.url_entry.grid(row=1, column=0, sticky="new")
        
        self.enter_button = tk.Button(left_frame, text="Enter", font=("Comic Sans MS", 10) ,command=self.storeUrl)
        self.enter_button.grid(row=2, column=0, sticky="new") 
        
        self.scrape_urls = tk.Button(left_frame, font=("Comic Sans MS", 10))
        self.scrape_urls["text"] = "Scrape\nURL"
        self.scrape_urls["command"] = self.startScraping
        self.scrape_urls.grid(row=3, column=0, columnspan=1, sticky="new")

        self.pages = [] # Stores the text for each page
        self.page_index = 0 # Stores the current page index

        self.page_label = tk.Label(left_frame, text="Current page number: {0}".format(self.page_index + 1), font=("Comic Sans MS", 10))
        self.page_label.grid(row=4, column=0, columnspan=1, sticky="new")

        self.prev_button = tk.Button(left_frame, text="<< Prev", font=("Comic Sans MS", 10),command=self.prevScrapedPage)
        self.prev_button.grid(row=5, column=0, sticky="new")

        self.next_button = tk.Button(left_frame, text="Next >>", font=("Comic Sans MS", 10), command=self.nextScrapedPage)
        self.next_button.grid(row=6, column=0, sticky="new")
        
        self.quit = tk.Button(left_frame, text="QUIT", font=("Comic Sans MS", 10), fg="red",
                              command=self.quitClient)
        self.quit.grid(row=8, column=0, columnspan=1, sticky="new")
        
        process_button = tk.Button(left_frame, text="Process Scraped Content", font=("Comic Sans MS", 10), command=lambda: self.showFrame(frame2))
        process_button.grid(row=7, column=0, sticky="new")
        
        # processing frame
        frame2 = tk.Frame(self.master)
        frame2.grid(row=0, column=0, sticky="nsew")

        left_frame2 = tk.Frame(frame2)
        left_frame2.grid(row=0, column=0, sticky="nsew")

        self.label2 = tk.Label(left_frame2, text="Article Summarizer", font=("Comic Sans MS", 20))
        self.label2.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.scrollbar2 = tk.Scrollbar(left_frame2)
        self.output2 = tk.Text(left_frame2, yscrollcommand=self.scrollbar2.set)
        self.scrollbar2.grid(row=0, column=2, rowspan=10, sticky="nsew")
        self.output2.grid(row=0, column=1, rowspan=10, sticky="nsew")
        self.scrollbar2.config(command=self.output2.yview)
        self.output2.config(state="disabled")

        self.ner_button = tk.Button(left_frame2, text="NER", font=("Comic Sans MS", 10), command=self.nerProcessing)
        self.ner_button.grid(row=1, column=0, sticky="new")

        self.topic_classification_button = tk.Button(left_frame2, text="Topic Classification", font=("Comic Sans MS", 10), command=self.topicClassification)
        self.topic_classification_button.grid(row=2, column=0, sticky="new")

        self.summarization_button = tk.Button(left_frame2, text="Summarization", font=("Comic Sans MS", 10), command=self.summarization)
        self.summarization_button.grid(row=3, column=0, sticky="new")

        self.page_label_processing = tk.Label(left_frame2, text="Current page number: {0}".format(self.page_index + 1), font=("Comic Sans MS", 10))
        self.page_label_processing.grid(row=4, column=0, columnspan=1, sticky="new")

        self.prev_button_processing = tk.Button(left_frame2, text="<< Prev", font=("Comic Sans MS", 10), command=self.prevScrapedPageProcessing)
        self.prev_button_processing.grid(row=5, column=0, sticky="new")

        self.next_button_processing = tk.Button(left_frame2, text="Next >>", font=("Comic Sans MS", 10), command=self.nextScrapedPageProcessing)
        self.next_button_processing.grid(row=6, column=0, sticky="new")

        back_button = tk.Button(left_frame2, text="Back", font=("Comic Sans MS", 10), command=lambda: self.showFrame(frame1))
        back_button.grid(row=7, column=0, sticky="new")

        quit_button = tk.Button(left_frame2, text="QUIT", font=("Comic Sans MS", 10), fg="red", command=self.quitClient)
        quit_button.grid(row=8, column=0, columnspan=1, sticky="new")
        
        self.showFrame(frame1)
        
    def showFrame(self, frame):
        frame.tkraise()
    
    def storeUrl(self):
        url = self.url_entry.get()
        if url and url != "Enter the Article URL:":
            self.urls.add(url)
            print(self.urls)
        self.url_entry.delete(0, 'end')
        
    def clearPlaceholder(self, event):
        if self.url_entry.get() == "Enter the Article URL:":
            self.url_entry.delete(0, "end")
            self.url_entry.config(fg="black")
            
    def updateOutput(self, text, chosen_output):
        self.clearOutput(chosen_output)
        chosen_output.config(state="normal")
        chosen_output.insert("end", text)
        chosen_output.config(state="disabled")
        
    def clearOutput(self, chosen_output):
        chosen_output.config(state="normal")
        chosen_output.delete("1.0", "end")
        chosen_output.config(state="disabled")
        
    def onScraping(self):
        self.scrape_urls["text"] = "Scraping..."
        self.scrape_urls["state"] = "disabled"
        self.enter_button["state"] = "disabled"
        
    def doneScraping(self):
        self.scrape_urls["text"] = "Scrape\nURL"
        self.scrape_urls["state"] = "normal"
        self.enter_button["state"] = "normal"
        
    def startScraping(self):
        #self.onScraping()
        self.loop.create_task(self.scrapeUrls(self.urls))
        
    def scrapeUrls(self, urls):
        self.scraper.scrape_urls(urls)
        self.onScrapingDone()
        
    def onScrapingDone(self):
        self.doneScraping()
        with open('output/output.json', 'r') as f:
            content = json.load(f)
            self.pages = [(idx, title, context) for idx, (title, context) in enumerate(content.items())]
            self.pagesScrapedFormat()
            
    def pagesScrapedFormat(self):
        self.updateOutput("Title: " + self.pages[self.page_index][1] + '\n\nArticle:\n' + self.pages[self.page_index][2], self.output)
    
    def prevScrapedPage(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.pagesScrapedFormat()
            self.page_label["text"] = "Current page number: {0}".format(self.page_index + 1)

    def nextScrapedPage(self):
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            self.pagesScrapedFormat()
            self.page_label["text"] = "Current page number: {0}".format(self.page_index + 1)
            
    def quitClient(self):
        if os.path.exists('output/output.json'):
            os.remove('output/output.json')
        self.master.destroy()
    
    def nerProcessing(self):
        self.process_status_code = 1
        if not self.process_data["ner"]:
            for page in self.pages:
                entities = self.ner.ner(page[2])
                entities_count = collections.Counter(entities)
                sorted_entities_count = sorted(entities_count.items(), key=lambda x:x[1], reverse=True)
                self.process_data["ner"].append(sorted_entities_count)
        self.nerFormat()
                
    def nerFormat(self):
        self.updateOutput("Most Mentioned Entities and Labels: \n\n" 
                          + "\n".join(["Mentioned Count: " + str(ner_data[1]) + "\nLabel: " 
                          + ner_data[0][1]  + "\nEntity: " + ner_data[0][0] + "\n"  for ner_data in self.process_data["ner"][self.page_index]])
                          , self.output2)
    
    def topicClassification(self):
        self.process_status_code = 2
        if not self.process_data["topic_classification"]:
            for page in self.pages:
                topic_classification = topic_model(page[2])
                self.process_data["topic_classification"].append(topic_classification)
        self.topicClassificationFormat()
    
    def topicClassificationFormat(self):
        self.updateOutput("Topic Classification: \n\n" + self.process_data["topic_classification"][self.page_index], self.output2)
    
    def summarization(self):
        self.process_status_code = 3
        if not self.process_data["summarize"]:
            for page in self.pages:
                summary = self.summarizer.summarize(page[2], 80)
                self.process_data["summarize"].append(summary)
        self.summaryFormat()
        
    def summaryFormat(self):
        self.updateOutput("Summary: \n\n" + self.process_data["summarize"][self.page_index], self.output2)
    
    def nextScrapedPageProcessing(self):
        if self.page_index < len(self.pages) - 1:
            self.page_index += 1
            if self.process_status_code == 1:
                self.nerProcessing()
            elif self.process_status_code == 2:
                self.topicClassificationFormat()
            elif self.process_status_code == 3:
                self.summaryFormat()
            self.page_label_processing["text"] = "Current page number: {0}".format(self.page_index + 1)
    
    def prevScrapedPageProcessing(self):
        if self.page_index > 0:
            self.page_index -= 1
            if self.process_status_code == 1:
                self.nerProcessing()
            elif self.process_status_code == 2:
                self.topicClassificationFormat()
            elif self.process_status_code == 3:
                self.summaryFormat()
            self.page_label_processing["text"] = "Current page number: {0}".format(self.page_index + 1)
    
loop = asyncio.get_event_loop()     
root = tk.Tk()
root.geometry("855x317")
root.title("Article Summarizer")
app = Application(master=root, loop=loop)
app.mainloop()
