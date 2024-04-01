import { Component, OnInit } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router';

@Component({
    templateUrl:'./listAll.component.html',
    styleUrls: ['./listAll.component.css']
})
export class ListAllComponent implements OnInit{
   
    UserId = "Test User"
    constructor(private route: ActivatedRoute,
    private router: Router) {}


    
    ngOnInit(): void {
        const id = Number(this.route.snapshot.paramMap.get('userId'));
      }
}