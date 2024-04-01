import { Injectable } from "@angular/core";
import { IUser } from "../Models/User";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Observable, tap, throwError, catchError, NotFoundError } from "rxjs";


@Injectable({
    providedIn: 'root'
})
export class FetchUserService
{
    private fetchUserUrl = "api/users_{userId}.json"

    constructor(private http: HttpClient) { }

    getUser(userId: string): Observable<IUser | undefined> {
        if(userId == null)
        {
            throw new Error(`User Id not passed`)
        }
        return this.http.get<IUser>(this.fetchUserUrl.replace("{userId}",userId)).pipe(
            tap(data => console.log("data: ", JSON.stringify(data))),
            catchError(this.handleError)
        );
    }

    private handleError(err: HttpErrorResponse): Observable<never> {
        // in a real world app, we may send the server to some remote logging infrastructure
        // instead of just logging it to the console
        let errorMessage = '';
        if (err.error instanceof ErrorEvent) {
          // A client-side or network error occurred. Handle it accordingly.
          errorMessage = `An error occurred: ${err.error.message}`;
        } else {
          // The backend returned an unsuccessful response code.
          // The response body may contain clues as to what went wrong,
          errorMessage = `Server returned code: ${err.status}, error message is: ${err.message}`;
        }
        console.error(errorMessage);
        return throwError(() => errorMessage);
    }
}

