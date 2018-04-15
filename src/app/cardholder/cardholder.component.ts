import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { HeroService } from '../hero.service';
import { TweetData, NewsData } from '../models';
import { HttpClient } from '@angular/common/http';

declare var $:any;

@Component({
  selector: 'app-cardholder',
  templateUrl: './cardholder.component.html',
  styleUrls: ['./cardholder.component.css']
})
export class CardholderComponent implements OnInit, OnChanges {
  @Input()
  public type: string;

  @Input()
  public query: string;

  public positive: number;

  public negative: number;

  public dataArray: Array<Object>;
  public instaDataArray: Array<Object>;
  constructor(private apiService: HeroService, private httpClient: HttpClient) {
    this.dataArray = undefined;
    this.instaDataArray = undefined;
   }

  ngOnInit() {
    console.log(this.type, this.query);
    this.fetchData();
  }

  ngOnChanges() {
    this.fetchData();
    this.dataArray = undefined;
    this.instaDataArray = undefined;
  }
  
  fetchData() {
    if (this.query !== undefined && this.query.length > 1) {
      if (this.type == "social") {
        this.apiService.getTwitterData(this.query, (error, response) => {
          if (this.dataArray === undefined) {
            this.dataArray = response as Array<Object>;
          }
        });
        this.apiService.getInstagramData(this.query, (error, response) => {
            if(this.instaDataArray === undefined) {

              this.instaDataArray = response as Array<Object>;
            }
        });
      }
      else if (this.type == "news") {
        this.apiService.getNewsData(this.query, (error, response) => {
          this.dataArray = response as Array<NewsData>;
          // Get NLP data
          this.httpClient.get("http://localhost:8000/data/sentiments/news/?token=" + this.apiService.fileToken)
          .subscribe((response) => {
              debugger
              this.positive = response["positive"];
              this.negative = response["negative"];
              this.apiService.fileToken = undefined;
          });
        });
      }
    }
  }

  changeProgressBar() {
    var percent = document.querySelector("percent");
    var input = document.querySelector("input");
    var value = this.positive;
    if(this.positive > this.negative) {
      value = this.positive;
    }
    else {
      value = this.negative;
    }
    input.addEventListener('change', function(){
      $.percent.style.setProperty('--percent', value) ;
    });
  }

}
