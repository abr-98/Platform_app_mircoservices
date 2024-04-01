import { HttpClientModule } from '@angular/common/http';
import { Component, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { AppComponent } from './app.component';
import { HomeComponent } from './Home/home.component'
import { ProfileComponent } from './Profile/profile.component';
import { FetchUserService } from './Services/user.services';
import { FormsModule } from '@angular/forms';
import { SignUpComponent } from './SignUp/signup.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ProfileComponent,
    SignUpComponent
    
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot([
     { path: 'home', component: HomeComponent},
     { path: 'profile/:userId', component: ProfileComponent},
     { path: 'signup', component: SignUpComponent},
     { path: '', redirectTo: 'home', pathMatch: 'full' },
     { path: '**', redirectTo: 'home', pathMatch: 'full' }
    ])
  ],
  providers: [FetchUserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
