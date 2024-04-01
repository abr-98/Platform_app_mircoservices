import { Component, OnInit } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router';
import { IUser } from '../Models/User';
import { FetchUserService } from '../Services/user.services';

@Component({
    templateUrl:'./profile.component.html',
    styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit{
    pageTitle = 'User Detail';
    errorMessage = '';
    user: IUser | undefined;

    constructor(private route: ActivatedRoute,
        private userService: FetchUserService) {
}


ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('userId')
    if (id) {
      this.getUser(id);
    }
  }

  getUser(userId: string): void {
    this.userService.getUser(userId).subscribe({
      next: user => this.user = user,
      error: err => this.errorMessage = err
    });
  }
}