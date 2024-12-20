import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './features/home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { MetadataComponent } from './features/metadata/metadata.component';
import { FilesComponent } from './features/files/files.component';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ReactiveFormsModule } from '@angular/forms'; // Uvezi ReactiveFormsModule
import { DecimalPipe } from '@angular/common'; // Dodaj ovo

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MetadataComponent,
    FilesComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MatSnackBarModule,
    BrowserAnimationsModule,
    ReactiveFormsModule 

  ],
  providers: [DecimalPipe], // Dodaj DecimalPipe ovde
  bootstrap: [AppComponent]
})
export class AppModule { }
