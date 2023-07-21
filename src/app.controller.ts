import { Controller, Get } from '@nestjs/common';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    const num = 35;
    const result = this.fibonacci(num);
    console.log(`Fibonacci ${num}: ${result}`);
    return `Hello World! Fibonacci ${num}: ${result}`;
  }

  fibonacci(n: number): number {
    if (n <= 1) return n;
    return this.fibonacci(n - 1) + this.fibonacci(n - 2);
  }
}
