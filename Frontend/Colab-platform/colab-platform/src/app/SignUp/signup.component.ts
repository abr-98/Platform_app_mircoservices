import { Component } from "@angular/core";
import { IUser } from "../Models/User";

@Component({
    templateUrl:'./signup.component.html',
    styleUrls: ['./signup.component.css']
})
export class SignUpComponent
{
    pageTitle = 'SignUp';
    errorMessage = '';

    private _user!: IUser;
    
    get user(): IUser {
        return this._user;
      }

    set user(value: IUser) {
    this._user = value;
    }
    
}
