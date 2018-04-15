import { Component, OnInit, Input, OnChanges } from '@angular/core';
import { HeroService } from '../hero.service';
import { TweetData, NewsData } from '../models';

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

  public dataArray: Array<Object>;
  public instaDataArray: Array<Object>;
  constructor(private apiService: HeroService) {
    this.dataArray = undefined;
    this.instaDataArray = undefined;
   }

  ngOnInit() {
    console.log(this.type, this.query);
    this.fetchData();
  }

  ngOnChanges() {
    this.fetchData()
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
        });
      }
    }
  }
}
