import { Component, OnInit, ViewChild, ElementRef, ViewChildren, ChangeDetectorRef } from '@angular/core';
import * as $ from 'jquery';
import { NgxSpinnerService } from 'ngx-spinner';
import { ApiCallerService } from '../services/api-caller.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cloud-detect',
  templateUrl: './cloud-detect.component.html',
  providers: [ NgxSpinnerService, ApiCallerService ],
  styleUrls: ['./cloud-detect.component.css']
})
export class CloudDetectComponent implements OnInit {

  baseUrl = 'http://76eac9623e94.ngrok.io/';

  detectionAlgorithm: string;
  imgPath: string;
  showWorkFlow1 = true;
  cloudTifPath = '';
  fileName = '';
  maskOutput = '';
  gifPath = '';
  mse = '';
  ssim = '';

  response = { };
  data = [];

  constructor(private spinner: NgxSpinnerService
    , private changeDetectorRef: ChangeDetectorRef
    , private _api: ApiCallerService
    , private router: Router) { }

  ngOnInit() {
    this._api.doGetRequest('/predictCloud').subscribe(res => {
      console.log(res);
      this.imgPath = this.baseUrl + res.image[1];
      this.maskOutput = this.baseUrl + res.image[2];
      this.gifPath = this.baseUrl + res.cnn[1];
      this.response = res;

      this.mse = parseFloat(this.response['cnn'][2]).toFixed(4);
      this.ssim = (parseFloat(this.response['cnn'][3]) * 100.0).toFixed(2) + '%';
      
      let i = 0;
      while (i < 3) {
        let element = this.response['kmeans'][i];
        // tslint:disable-next-line: no-shadowed-variable
        const list = [];
        list.push(element[0]);
        element[1] = parseFloat(element[1]).toFixed(2);
        list.push(element[1]);
        element[2] = parseFloat(element[2]).toFixed(2);
        list.push(element[2]);
        list.push(element[5]);

        element = this.response['mpa'][i];
        element[1] = parseFloat(element[1]).toFixed(2);
        list.push(element[1]);
        element[2] = parseFloat(element[2]).toFixed(2);
        list.push(element[2]);
        element[3] = parseFloat(element[3]).toFixed(2);
        list.push(element[3]);

        this.data.push(list);
        i++;
      }

      console.log(this.data);
      this.cloudTifPath = this.response['image'][0];
      this.fileName = this.response['image'][4].split('.')[0];
      console.log(this.fileName);
      this.drawCanvas(this.imgPath);
      const canvas = document.querySelector('canvas');
      const ctx = canvas.getContext('2d');
      // ctx.clearRect(0, 0, canvas.width, canvas.height);
      canvas.addEventListener('mousedown', this.placeMarker.bind(this));
    });
  }

  placeMarker(e) {
    const c = <HTMLCanvasElement>document.getElementById('myCanvas');
    const ctx = c.getContext('2d');
    const rect = c.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const marker = new Image();
    marker.src = 'https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png';
    ctx.drawImage(marker, x, y, 25, 25);
    this.getCloudFeatures(y, x, ctx);
  }

  getCloudFeatures(x: number, y: number, ctx: CanvasRenderingContext2D) {
    this._api.doPostRequest('/predictCloud', 
      { 'posx': (x * (984 / 575)).toFixed(0), 'posy': (y * (1074 / 575)).toFixed(0), 'imageName': this.fileName }).subscribe(res => {
        console.log(res);
        ctx.font = '15px Calibri';
        let markerText = '';
        if (res['cloudy']) {
          markerText = 'Mask: ' + res['mask'] + ', Type: ' + res['type'];
        } else {
          markerText = 'Not A Cloud!';
        }
        ctx.fillStyle = 'red';
        ctx.fillText(markerText, x, y + 15);
    });
  }

  drawCanvas(imgPath) {
    // if (document.getElementById('canvasDiv').childElementCount <= 0) {
    //   document.getElementById('canvasDiv').append('<canvas id="myCanvas"></canvas>');
    // }
    const c = <HTMLCanvasElement>document.getElementById('myCanvas');
    const ctx = c.getContext('2d');
    const img = new Image();
    img.onload = function() {
      c.width = 575;
      c.height = 575;
      ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 575, 575);
    };
    img.src = imgPath;
  }

  clearCanvas() {
    const c = <HTMLCanvasElement>document.getElementById('myCanvas');
    const ctx = c.getContext('2d');
    ctx.clearRect(0, 0, c.width, c.height);
    this.drawCanvas(this.imgPath);
  }

  getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    console.log('x: ' + x + ' y: ' + y);
  }

  // dispatchHookOnCanvasClick() {
  //   document.getElementById('myCanvas').onclick = function(event) {
  //     // if(document.getElementById('marker') !== undefined) {
  //     //   document.getElementById('marker').remove();
  //     // }
  //     var marker = document.createElement('div');
  //     marker.setAttribute("id","marker");
  //     marker.style.position = 'absolute';
  //     marker.style.top = event.pageY + 'px';
  //     marker.style.left = event.pageX + 'px';
  //     marker.style.width = '25px';
  //     marker.style.height = '25px';
  //     // marker.style.backgroundImage = "url('https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678111-map-marker-512.png')";
  //     marker.style.background = "#000";
  //     document.getElementsByTagName('canvas')[0].append(marker);
  //   };
  // }

  // dispatchHookOnW1() {
    // this.changeDetectorRef.detectChanges();
    // $(this.w1.nativeElement)
    //   .on('click', (event) => {
    //     this.spinner.show();
    //     this.x = event.pageX - this.w1.nativeElement.offsetLeft;
    //     this.y = event.pageY - this.w1.nativeElement.offsetTop;
    //     console.log("("+this.x+","+this.y+")");
    //     setTimeout(() => {
    //       this.spinner.hide();
    //     }, 2000);
    //   });
  // }

  // dispatchHookOnW2() {
  //   this.changeDetectorRef.detectChanges();
  //   $(this.w2.nativeElement)
  //     .on('click', (event) => {
  //       this.spinner.show();
  //       this.x = event.pageX - this.w2.nativeElement.offsetLeft;
  //       this.y = event.pageY - this.w2.nativeElement.offsetTop;
  //       console.log("("+this.x+","+this.y+")");
  //       setTimeout(() => {
  //         this.spinner.hide();
  //       }, 2000);
  //     });
  // }

  // ngAfterViewInit() {
  //   this.dispatchHookOnW1();
  // }

  // selectDetectionAlgo() {
  //   console.log(this.detectionAlgorithm);
  //   this.imgPath = '../assets/img/' + this.detectionAlgorithm;
  // }

  toggleWorkFlow() {
    this.showWorkFlow1 = !this.showWorkFlow1;
    if (this.showWorkFlow1) {
      this.router.routeReuseStrategy.shouldReuseRoute = () => false;
      this.router.onSameUrlNavigation = 'reload';
      this.router.navigate(['/detect']);
    }
  }

}
