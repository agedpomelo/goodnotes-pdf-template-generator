# GoodNotes PDF Template Generator

The GoodNotes PDF Template Generator is a Python project that allows you to generate PDF templates larger than A4 for use with GoodNotes notebooks. This tool helps you create custom-sized templates based on standard paper sizes, such as A0, A1, A2, A3, A4, or generate templates for all available sizes.

## Requirements

- Python 3.x

## Usage

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/agedpomelo/goodnotes-pdf-template-generator
   ```

2. Navigate to the project directory:

   ```
   cd goodnotes-pdf-template-generator
   ```

3. Run the script with the desired paper size:

   ```
   python paper.py <paper_size>
   ```

   Available paper sizes: A0, A1, A2, A3, A4, ALL

   For example:

   ```
   python paper.py A3
   ```

4. The generated PDF templates will be stored in the `out` directory.

## Output

The generated PDF templates will be saved in the `out` directory. Each template will be named according to the paper size, e.g., `A3 WHITE GRID.pdf`. If you generate templates for all available sizes, individual files will be created for each size.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request.

## Acknowledgements

This project was inspired by the need for custom-sized templates for GoodNotes notebooks. We would like to acknowledge the contributors who have helped make this project better.

## Contact

For any inquiries or feedback, please contact us at [agedpomelo@gmail.com](mailto:agedpomelo@gmail.com).

Happy template generation!