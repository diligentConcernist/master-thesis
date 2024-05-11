import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainPageComponent } from "./components/main-page/main-page.component";
import {
    BookRecommendationPageComponent
} from "./components/book-recommendation-page/book-recommendation-page.component";

const routes: Routes = [
    { path: "", component: MainPageComponent },
    { path: "book/:book_title", component: BookRecommendationPageComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
