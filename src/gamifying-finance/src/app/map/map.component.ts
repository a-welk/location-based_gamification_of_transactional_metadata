import { Component, ElementRef, Inject, OnInit, PLATFORM_ID, ViewChild } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { GoogleMap, GoogleMapsModule } from '@angular/google-maps';
import { Loader } from '@googlemaps/js-api-loader';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [CommonModule, GoogleMapsModule],
  templateUrl: './map.component.html',
  styleUrl: './map.component.css'
})

export class MapComponent implements OnInit {
  @ViewChild('mapContainer', { static: false })
  gmap!: ElementRef;

  map!: google.maps.Map;

  ngOnInit() {

  }

  ngAfterViewInit() {
    this.mapInitializer();
  }

  mapInitializer() {
    this.map = new google.maps.Map(this.gmap.nativeElement, {
      center: { lat: 41.3851, lng: 2.1734 },
      zoom: 12
    });
    
  }
}
