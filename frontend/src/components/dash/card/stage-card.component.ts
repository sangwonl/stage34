import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';

import { Stage } from '../../../models/Stage';

import { TimeAgoPipe } from 'angular2-moment';

@Component({
    selector: 'stage-card',
    templateUrl: 'stage-card.component.html',
    styleUrls: ['stage-card.component.css'],
    pipes: [TimeAgoPipe]
})
export class StageCardComponent implements OnInit {
    @Input() stage: Stage;
    @Output() infoClick = new EventEmitter();
    @Output() statusClick = new EventEmitter();

    constructor() {}

    ngOnInit() {}

    onInfoClicked() {
        this.infoClick.emit({value: this.stage});
    }

    onStatusClicked() {
        this.statusClick.emit({value: this.stage});
    }
}