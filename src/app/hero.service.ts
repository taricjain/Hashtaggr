import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { CallbackInterface, TweetData, InstagramData, NewsData } from './models';

@Injectable()
export class HeroService {

  public fileToken: string;

  constructor(private httpService: HttpClient) { }

  getTwitterData(searchTag: string, callback: CallbackInterface): void {
    this.httpService.get<Object[]>("http://localhost:8000/data/twitter/?query=" + searchTag)
    .subscribe(
      (response) => {
        var twitterData = new Array<TweetData>();
        response.forEach(element => {
          twitterData.push(element as TweetData);
        });
       callback(null, twitterData); 
      }
    );
  }

  getInstagramData(searchTag: string, callback: CallbackInterface) {
    this.httpService.get<Object[]>("http://localhost:8000/data/instagram/?query=" + searchTag)
    .subscribe(
      (response) => {
        var instagramData = new Array<InstagramData>();
        response['data'].forEach(element => {
          var item = {} as InstagramData;
          item.caption = element["text"]
          item.picture = element["display_url"]
          instagramData.push(item);
        });

        callback(null, instagramData);
      }
    );
  }

  getNewsData(searchTag: string, callback: CallbackInterface) {
    this.httpService.get("http://localhost:8000/data/news/?query=" + searchTag)
    .subscribe((response) => {
      this.fileToken = response["token"];
      var newsData = new Array<NewsData>();
      response["data"]["articles"].forEach(element => {
        var newsDataObj = {} as NewsData;
        newsDataObj.title = element["title"];
        newsDataObj.source = element["source"]["name"];
        newsDataObj.description = element["description"]
        newsDataObj.url = element["url"];
        newsDataObj.imageUrl = element["urlToImage"];
        newsData.push(newsDataObj);
      });

      callback(null, newsData);
    });
  }

  
}
