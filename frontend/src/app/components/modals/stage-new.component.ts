import { Component, Output, EventEmitter, ViewChild, AfterViewInit } from '@angular/core';
import { ModalDirective } from 'ng2-bootstrap';

import { GithubService } from '../../services/github.service';
import { Repo, Branch } from '../../models/repo';

@Component({
  selector: 'stage-new',
  templateUrl: 'stage-new.component.html',
  styleUrls: ['stage-new.component.scss']
})
export class StageNewComponent implements AfterViewInit {
  private title: string = '';
  private repo: Repo = null;
  private branch: Branch = null;
  private runOnClose: boolean = true;

  private repos: Repo[];
  private branches: Branch[];

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
    this.githubService.getBranches(this.repo).then(branches => this.branches = branches);
  }

  private onChangeBranch(selectedBranch: Branch) {
    this.branch = selectedBranch;
  }

  private resetForm() {
    this.title = '';
    this.repo = null;
    this.branch = null;
  }

    private onSubmit() {
      this.createNew.emit({
        value: {
          title: this.title,
          repo: this.repo,
          branch: this.branch,
          runOnClose: this.runOnClose
        }
      });
      this.hideModal();
      this.resetForm();
    }
}