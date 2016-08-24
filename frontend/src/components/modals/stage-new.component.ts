import { Component, Output, EventEmitter, ViewChild, AfterViewInit } from '@angular/core';
import { ModalDirective, MODAL_DIRECTIVES, BS_VIEW_PROVIDERS } from 'ng2-bootstrap';
import { CORE_DIRECTIVES } from '@angular/common';

import { GithubService } from '../../services/github.service';
import { Repo } from '../../models/repo';

@Component({
    selector: 'stage-new',
    templateUrl: 'stage-new.component.html',
    styleUrls: ['stage-new.component.css'],
    directives: [MODAL_DIRECTIVES, CORE_DIRECTIVES],
    viewProviders: [BS_VIEW_PROVIDERS],
    providers: [GithubService]
})
export class StageNewComponent implements AfterViewInit {
    private title: string = '';
    private repo: Repo = null;
    private branch: string = '';
    private runOnClose: boolean = true;

    private repos: Repo[];

    @ViewChild('newModal') newModal: ModalDirective;
    @Output() createNew = new EventEmitter();

    constructor(private githubService: GithubService) {}
 
    ngAfterViewInit() {
        this.githubService.getRepositories().then(repos => this.repos = repos);
    }

    public showModal() { this.newModal.show(); }
    public hideModal() { this.newModal.hide(); }

    private onChangeRepo(selectedRepo: Repo) {
        this.repo = selectedRepo;

        // here load branches..
    }

    private resetForm() {
        this.title = ''; 
        this.repo = null; 
        this.branch = ''; 
    }

    private onSubmit() {
        this.createNew.emit({
            value: {
                title: this.title,
                repo: this.repo.full_name,
                branch: this.branch,
                runOnClose: this.runOnClose
            }
        });
        this.hideModal();
        this.resetForm();
    }
}