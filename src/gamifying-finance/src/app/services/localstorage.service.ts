import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';
import { PLATFORM_ID, Inject } from '@angular/core';

class LocalStorage implements Storage {
  [name: string]: any;
  private store: {[key: string]: string} = {};
  get length(): number {
    return Object.keys(this.store).length;
  }
  clear(): void {
    this.store = {};
  }
  getItem(key: string): string | null {
    return this.store[key] || null;
  }
  key(index: number): string | null {
    const keys = Object.keys(this.store);
    return keys[index] || null;
  }
  removeItem(key: string): void {
    delete this.store[key];
  }
  setItem(key: string, value: string): void {
    this.store[key] = value;
  }
}

@Injectable({
  providedIn: 'root'
})
export class LocalstorageService implements Storage {
  private storage: Storage;
  private isBrowser: BehaviorSubject<boolean>;

  constructor(@Inject(PLATFORM_ID) private platformId: any) {
    this.isBrowser = new BehaviorSubject<boolean>(isPlatformBrowser(platformId));
    this.storage = new LocalStorage();

    this.isBrowser.subscribe(isBrowser => {
      if (isBrowser) {
        this.storage = localStorage;
      }
    });
  }

  get length(): number {
    return this.storage.length;
  }

  clear(): void {
    this.storage.clear();
  }

  getItem(key: string): string | null {
    return this.storage.getItem(key);
  }

  key(index: number): string | null {
    return this.storage.key(index);
  }

  removeItem(key: string): void {
    this.storage.removeItem(key);
  }

  setItem(key: string, value: string): void {
    this.storage.setItem(key, value);
  }
}
