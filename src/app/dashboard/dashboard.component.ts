import { Component, OnInit } from '@angular/core';
import { HeroService } from '../hero.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  public searchQuery: string;

  constructor(private apiService: HeroService) { }

  ngOnInit() { }

  submitSearchQuery(query: string) {
    this.searchQuery = query;
    console.log(query);
  }
}
